import json

from bot.services import BaseService
from bot.utils import RedisKeys


class PackService(BaseService):
    async def _get_packs_from_db(self) -> list:
        return await self._request(
            method="GET",
            endpoint="packs/",
        )

    async def _set_packs_to_redis(self, packs: list) -> None:
        return await self.redis.setex(
            RedisKeys.packs(),
            60 * 60 * 12,
            json.dumps(packs, ensure_ascii=False),
        )

    async def _get_packs_from_redis(self) -> list | None:
        return await self.redis.get(RedisKeys.packs())

    async def get_packs(self) -> list:
        cached = await self._get_packs_from_redis()

        if cached:
            return json.loads(cached)

        packs = await self._get_packs_from_db()
        await self._set_packs_to_redis(packs)
        return packs
