from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, User


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, redis):
        super().__init__()
        self.redis = redis
        self.rate_limits = {
            "Message": 1.0,
            "CallbackQuery": 0.5,
        }

    async def __call__(self, handler, event, data: dict):
        """Apply rate limiting based on event type."""
        user: User | None = data.get("event_from_user")

        if user is None:
            return await handler(event, data)

        event_name = event.__class__.__name__
        rate = self.rate_limits.get(event_name)

        if rate is None:
            return await handler(event, data)

        key = f"throttle:{user.id}:{event_name}"

        allowed = await self.redis.set(
            key,
            "1",
            px=int(rate * 1000),
            nx=True,
        )

        if not allowed:
            if isinstance(event, CallbackQuery):
                await event.answer("⏳ Слишком часто!")

            return None

        return await handler(event, data)
