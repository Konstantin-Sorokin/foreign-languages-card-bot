import time

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from redis.asyncio import Redis


class ThrottlingMiddleware(BaseMiddleware):
    """
    Ограничивает частоту запросов от пользователя.

    Лимиты (можно настроить через rate_limits):
      - Message: 1 запрос в секунду
      - CallbackQuery: 1 запрос в 0.5 секунды

    При превышении лимита запрос игнорируется (return без вызова handler).
    Для CallbackQuery обязательно отправляется event.answer(), чтобы Telegram не ждал.
    """

    def __init__(self, redis: Redis):
        super().__init__()
        self.redis = redis
        self.rate_limits = {
            Message: 1.0,
            CallbackQuery: 0.5,
        }

    async def __call__(self, handler, event, data: dict):
        """Обрабатывает входящее событие: проверяет лимит и либо пропускает, либо блокирует."""
        if not hasattr(event, "from_user") or event.from_user is None:
            return await handler(event, data)

        rate = self.rate_limits.get(type(event))
        if rate is None:
            return await handler(event, data)

        user_id = event.from_user.id
        key = f"throttle:{user_id}"
        last = await self.redis.get(key)
        now = time.time()

        if last is not None and (now - float(last)) < rate:
            if isinstance(event, CallbackQuery):
                await event.answer("⏳ Слишком часто!", show_alert=False)
            return

        await self.redis.setex(key, 5, str(now))
        return await handler(event, data)
