from aiogram import BaseMiddleware
from aiogram.types import User

from bot.services.user import UserService


class UserMiddleware(BaseMiddleware):
    def __init__(self, user_service: UserService):
        self._user_service = user_service

    async def __call__(self, handler, event, data):
        """Inject the internal user ID into the event data."""
        user: User | None = data.get("event_from_user")

        if user is None:
            return await handler(event, data)

        data["user_id"] = await self._user_service.get_user_id(user.id)

        return await handler(event, data)
