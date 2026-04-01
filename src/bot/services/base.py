import aiohttp
import redis.asyncio as redis

from bot.utils import settings


class BaseService:
    def __init__(self, redis_client: redis.Redis | None = None):
        self.base_url = settings.api_url
        self.redis = redis_client

    async def _request(self, method: str, endpoint: str, **kwargs):
        url = f"{self.base_url}{endpoint}"
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, **kwargs) as response:
                return await response.json()
