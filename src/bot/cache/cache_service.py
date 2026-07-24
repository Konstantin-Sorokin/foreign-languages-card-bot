import json

import redis.asyncio as redis


class CacheService:
    def __init__(self, redis_client: redis.Redis):
        self._redis = redis_client

    async def get(self, key: str):
        """Get a cached JSON value by key."""
        data = await self._redis.get(key)
        return None if data is None else json.loads(data)

    async def set(self, key: str, value, ttl: int):
        """Cache a value with expiration time in seconds."""
        await self._redis.set(key, json.dumps(value), ex=ttl)

    async def delete(self, key: str):
        """Remove a cached value."""
        await self._redis.delete(key)

    async def push_list(self, key: str, values: list, ttl: int | None = None):
        """Push multiple values to a list and optionally set TTL."""
        if values:
            await self._redis.rpush(key, *[json.dumps(value) for value in values])

        if ttl is not None:
            await self._redis.expire(key, ttl)

    async def append_list(self, key: str, value: dict):
        """Append a single value to a list."""
        await self._redis.rpush(key, json.dumps(value))

    async def lpop(self, key: str):
        """Pop the first element from a list."""
        value = await self._redis.lpop(key)

        if value is None:
            return None

        return json.loads(value)
