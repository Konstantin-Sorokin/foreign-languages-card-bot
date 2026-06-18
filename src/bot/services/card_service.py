import json

from bot.services import BaseService
from bot.utils import RedisKeys


class CardService(BaseService):
    async def initialize_learning_queue(self, telegram_id: int, user_id: int) -> bool:
        """
        Загружает карточки пользователя из API в Redis-очередь.

        1. Запрашивает карточки из API по user_id.
        2. Если карточки есть — очищает текущую очередь в Redis и загружает новые карточки.
        3. Если карточек нет — возвращает False, чтобы бот мог отреагировать соответствующим сообщением.

        Returns:
            True, если карточки найдены и загружены, False — если карточек нет.
        """
        cards = await self._request(method="GET", endpoint=f"users/{user_id}/progress/")

        if not cards:
            return False

        queue_key = RedisKeys.user_cards(telegram_id)
        await self.redis.delete(queue_key)
        await self.add_cards_to_queue(telegram_id, cards)
        return True

    async def get_next_card_from_queue(self, telegram_id: int) -> dict | None:
        """
        Извлекает следующую карточку из начала очереди (LPOP).

        Returns:
            Словарь с данными карточки или None, если очередь пуста.
        """
        queue_key = RedisKeys.user_cards(telegram_id)
        cache_card = await self.redis.lpop(queue_key)
        return json.loads(cache_card) if cache_card else None

    async def add_card_to_the_end_queue(self, telegram_id: int, card: dict) -> None:
        """
        Добавляет карточку в конец очереди (RPUSH).
        Используется, когда пользователь не знает карточку — она возвращается в конец для повторения.
        """
        queue_key = RedisKeys.user_cards(telegram_id)
        return await self.redis.rpush(queue_key, json.dumps(card, ensure_ascii=False))

    async def add_cards_to_queue(self, telegram_id: int, cards: list[dict]) -> None:
        """Кэширует список карточек пользователя в очередь Redis на время TTL."""
        TTL = 60 * 60  # 1 час
        queue_key = RedisKeys.user_cards(telegram_id)
        pipe = self.redis.pipeline()
        for card in cards:
            pipe.rpush(queue_key, json.dumps(card, ensure_ascii=False))
        await pipe.expire(queue_key, TTL)
        await pipe.execute()
