from bot.services import BaseService
from bot.utils import RedisKeys


class UserService(BaseService):
    async def _get_or_create_user(self, telegram_id: int):
        return await self._request(
            method="POST",
            endpoint="users/",
            json={"telegram_id": telegram_id},
        )

    async def _get_user_from_redis(self, telegram_id: int):
        return await self.redis.get(RedisKeys.user_id(telegram_id))

    async def _set_user_to_redis(self, telegram_id: int, user_id: int):
        return await self.redis.setex(
            RedisKeys.user_id(telegram_id),
            604800,
            str(user_id),
        )

    async def get_user_id(self, telegram_id: int) -> int:
        cached = await self._get_user_from_redis(telegram_id)
        if cached:
            return int(cached)

        user: dict = await self._get_or_create_user(telegram_id)
        user_id = user.get("id")

        await self._set_user_to_redis(telegram_id, user_id)
        return user_id
