import aiohttp
import redis.asyncio as redis

from bot.utils import settings


class BaseService:
    def __init__(self, redis_client: redis.Redis | None = None):
        self.base_url = settings.api_url
        self.redis = redis_client
        self._session: aiohttp.ClientSession | None = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=30)
            self._session = aiohttp.ClientSession(timeout=timeout)
        return self._session

    async def _request(self, method: str, endpoint: str, **kwargs):
        url = f"{self.base_url}{endpoint}"
        session = await self._get_session()
        async with session.request(method, url, **kwargs) as response:
            response.raise_for_status()
            return await response.json()

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()