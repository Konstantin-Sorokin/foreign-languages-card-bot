import aiohttp


class BaseApiClient:
    def __init__(
        self,
        session: aiohttp.ClientSession,
        base_url: str,
    ):
        self._session = session
        self._base_url = base_url.rstrip("/")

    async def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs,
    ):
        """Execute an HTTP request and return parsed JSON response."""
        url = f"{self._base_url}/{endpoint.lstrip('/')}"

        async with self._session.request(
            method,
            url,
            **kwargs,
        ) as response:
            response.raise_for_status()

            if response.status == 204:
                return None

            return await response.json()

    async def get(self, endpoint: str, **kwargs):
        return await self._request("GET", endpoint, **kwargs)

    async def post(self, endpoint: str, **kwargs):
        return await self._request("POST", endpoint, **kwargs)

    async def patch(self, endpoint: str, **kwargs):
        return await self._request("PATCH", endpoint, **kwargs)

    async def delete(self, endpoint: str, **kwargs):
        return await self._request("DELETE", endpoint, **kwargs)
