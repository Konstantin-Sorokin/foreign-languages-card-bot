import json

from bot.services import BaseService
from bot.utils import RedisKeys


class CardService(BaseService):
    async def initialize_learning_queue(self, telegram_id: int, user_id: int) -> bool:
        """
        Загружает карточки из БД в Redis.
        Возвращает True, если карточки найдены.
        """
        queue_key = RedisKeys.user_cards(telegram_id)

        await self.redis.delete(queue_key)

        cards = await self._request(method="GET", endpoint=f"users/{user_id}/progress/")

        if not cards:
            return False

        await self.add_cards_to_queue(telegram_id, cards)
        return True

    async def get_next_card_from_queue(self, telegram_id: int) -> dict | None:
        """Достает следующую(первую слева) карту из Redis."""
        queue_key = RedisKeys.user_cards(telegram_id)
        cache_card = await self.redis.lpop(queue_key)
        return json.loads(cache_card) if cache_card else None

    async def add_card_to_the_end_queue(self, telegram_id: int, card: dict):
        """Кладет карту в конец очереди Redis.
        Функция нужна в момент, когда пользователь не знает карточку"""
        queue_key = RedisKeys.user_cards(telegram_id)
        return await self.redis.rpush(queue_key, json.dumps(card, ensure_ascii=False))

    async def add_cards_to_queue(self, telegram_id: int, cards: list[dict]):
        """Кладет карту в начало очереди Redis."""
        queue_key = RedisKeys.user_cards(telegram_id)
        pipe = self.redis.pipeline()
        for card in cards:
            pipe.rpush(queue_key, json.dumps(card, ensure_ascii=False))
        await pipe.execute()

    async def load_pack_verbs_to_cache(self, telegram_id: int, pack_id: int):
        """Берет все паки для неправильных глаголов из БД и добавляет в Redis"""
        cards: list[dict] = await self._request(
            method="GET",
            endpoint=f"packs/{pack_id}/cards/",
        )
        await self.redis.setex(
            RedisKeys.user_verbs(telegram_id),
            1800,
            json.dumps(cards, ensure_ascii=False),
        )
