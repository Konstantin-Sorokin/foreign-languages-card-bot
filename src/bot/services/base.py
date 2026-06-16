import aiohttp
import redis.asyncio as redis

from bot.utils import settings


class BaseService:
    def __init__(self, redis_client: redis.Redis | None = None):
        self.base_url = settings.api_url
        self.redis = redis_client
        self._session: aiohttp.ClientSession | None = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """
        Возвращает переиспользуемую HTTP-сессию.

        Создаёт новую сессию с таймаутом 30 секунд, если она ещё не создана или была закрыта.
        """
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=30)
            self._session = aiohttp.ClientSession(timeout=timeout)
        return self._session

    async def _request(self, method: str, endpoint: str, **kwargs):
        """
        Отправляет HTTP-запрос к API.

        Args:
            method: HTTP-метод (GET, POST, PATCH и т.д.).
            endpoint: Путь к endpoint'у (например, "users/" или "packs/1/cards/").
            **kwargs: Дополнительные параметры для aiohttp-запроса (json, params и т.д.).

        Returns:
            Ответ API, декодированный из JSON.

        Raises:
            aiohttp.ClientResponseError: при HTTP-статусе 4xx или 5xx.
        """
        url = f"{self.base_url}{endpoint}"
        session = await self._get_session()
        async with session.request(method, url, **kwargs) as response:
            response.raise_for_status()
            return await response.json()

    async def close(self):
        """Закрывает HTTP-сессию, если она была открыта."""
        if self._session and not self._session.closed:
            await self._session.close()
