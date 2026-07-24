from bot.api.users import UserApi
from bot.cache.cache_keys import CacheKey
from bot.cache.cache_service import CacheService
from bot.schemas.user import UserCreate


class UserService:
    def __init__(self, user_api: UserApi, cache: CacheService):
        self._user_api = user_api
        self.cache = cache

    async def get_user_id(self, telegram_id: int) -> int:
        """Resolve internal user ID from Telegram ID, using cache when possible."""

        key = CacheKey.user_db_id(telegram_id)

        user_id = await self.cache.get(key)

        if user_id is not None:
            return user_id

        user = await self._user_api.get_or_create(UserCreate(telegram_id=telegram_id))

        await self.cache.set(key, user.id, ttl=86400)

        return user.id
