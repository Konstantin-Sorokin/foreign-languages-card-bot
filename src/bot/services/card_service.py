import json

from bot.services import BaseService
from bot.utils import RedisKeys


class CardService(BaseService):
    async def get_next_translation_card(
        self, telegram_id: int, user_id: int
    ) -> dict | None:
        queue_key = RedisKeys.user_cards(telegram_id)

        cache_card = await self.redis.lpop(queue_key)
        if cache_card:
            return json.loads(cache_card)

        db_cards = await self._request(
            method="GET",
            endpoint=f"users/{user_id}/progress/",
        )

        if not db_cards:
            return None

        await self.add_cards_to_queue(telegram_id, cards=db_cards)

        cache_card = await self.redis.lpop(queue_key)
        return json.loads(cache_card)

    async def add_card_to_the_end_queue(self, telegram_id: int, card: dict):
        queue_key = RedisKeys.user_cards(telegram_id)
        return await self.redis.rpush(queue_key, json.dumps(card, ensure_ascii=False))

    async def add_cards_to_queue(self, telegram_id: int, cards: list[dict]):
        queue_key = RedisKeys.user_cards(telegram_id)
        pipe = self.redis.pipeline()
        for card in cards:
            pipe.rpush(queue_key, json.dumps(card, ensure_ascii=False))
        await pipe.execute()

    async def load_pack_verbs_to_cache(self, telegram_id: int, pack_id: int):
        cards: list[dict] = await self._request(
            method="GET",
            endpoint=f"packs/{pack_id}/cards/",
        )
        await self.redis.setex(
            RedisKeys.user_verbs(telegram_id),
            1800,
            json.dumps(cards, ensure_ascii=False),
        )
