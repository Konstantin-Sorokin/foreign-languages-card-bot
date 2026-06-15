import time

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from redis.asyncio import Redis


class ThrottlingMiddleware(BaseMiddleware):
    """
    Middleware для ограничения частоты запросов от пользователя (anti-spam).

    Лимиты:
      - Message: 1 запрос в секунду
      - CallbackQuery: 1 запрос в 0.5 секунды

    При превышении лимита запрос игнорируется.
    Для CallbackQuery обязательно отвечаем event.answer(), чтобы Telegram не ждал.
    Для Message вызываем event.answer() с сообщением о превышении лимита.
    """

    def __init__(self, redis: Redis):
        super().__init__()
        self.redis = redis
        self.rate_limits = {
            Message: 1.0,
            CallbackQuery: 0.5,
        }

    async def __call__(self, handler, event, data: dict):
        # Пропускаем события без from_user
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
            # Превышен лимит — отвечаем, чтобы Telegram не ждал, и игнорируем
            if isinstance(event, CallbackQuery):
                await event.answer("⏳ Слишком часто!", show_alert=False)
            return

        await self.redis.setex(key, 5, str(now))
        return await handler(event, data)