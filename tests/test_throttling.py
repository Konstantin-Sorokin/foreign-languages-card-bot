import time
from unittest.mock import AsyncMock, MagicMock

import pytest
from aiogram.types import CallbackQuery

from bot.middlewares.throttling import ThrottlingMiddleware


@pytest.fixture
def mock_handler():
    """Мок handler, который возвращает заглушку."""
    handler = AsyncMock()
    handler.return_value = "handler_result"
    return handler


@pytest.fixture
def mock_event_no_user():
    """Событие без from_user (например, ChatMemberUpdated)."""
    event = MagicMock()
    del event.from_user
    return event


class TestThrottlingMiddleware:
    """Тесты для ThrottlingMiddleware."""

    @staticmethod
    def _make_event(user_id=12345):
        """Создаёт мок-событие с указанным user_id."""
        event = MagicMock()
        event.from_user = MagicMock()
        event.from_user.id = user_id
        return event

    @staticmethod
    def _make_callback_event(user_id=12345):
        """
        Создаёт мок-событие, которое isinstance(event, CallbackQuery) вернёт True.
        Нужно для проверки вызова event.answer() при блокировке.
        """
        event = MagicMock(spec=CallbackQuery)
        event.from_user = MagicMock()
        event.from_user.id = user_id
        event.answer = AsyncMock()
        return event

    async def test_no_from_user_passes(
        self, mock_redis, mock_handler, mock_event_no_user
    ):
        """Событие без from_user → handler вызывается."""
        middleware = ThrottlingMiddleware(mock_redis)
        result = await middleware(mock_handler, mock_event_no_user, {})

        assert result == "handler_result"
        mock_handler.assert_awaited_once_with(mock_event_no_user, {})

    async def test_unknown_event_type_passes(self, mock_redis, mock_handler):
        """Тип события не зарегистрирован в rate_limits → handler вызывается."""
        event = self._make_event()

        middleware = ThrottlingMiddleware(mock_redis)
        middleware.rate_limits = {}
        result = await middleware(mock_handler, event, {})

        assert result == "handler_result"
        mock_handler.assert_awaited_once_with(event, {})

    async def test_first_request_passes(self, mock_redis, mock_handler):
        """Первый запрос (Redis None) → handler вызывается + setex."""
        event = self._make_event()

        middleware = ThrottlingMiddleware(mock_redis)
        middleware.rate_limits = {type(event): 1.0}
        mock_redis.get.return_value = None

        result = await middleware(mock_handler, event, {})

        assert result == "handler_result"
        mock_handler.assert_awaited_once_with(event, {})
        mock_redis.setex.assert_awaited_once()

    async def test_request_within_limit_blocked(self, mock_redis, mock_handler):
        """Запрос в пределах лимита → handler НЕ вызывается."""
        event = self._make_event()

        middleware = ThrottlingMiddleware(mock_redis)
        middleware.rate_limits = {type(event): 1.0}
        mock_redis.get.return_value = str(time.time())

        await middleware(mock_handler, event, {})

        mock_handler.assert_not_awaited()

    async def test_request_after_limit_passes(self, mock_redis, mock_handler):
        """Запрос после истечения лимита → handler вызывается."""
        event = self._make_event()

        middleware = ThrottlingMiddleware(mock_redis)
        middleware.rate_limits = {type(event): 1.0}
        mock_redis.get.return_value = str(time.time() - 2.0)

        result = await middleware(mock_handler, event, {})

        assert result == "handler_result"
        mock_handler.assert_awaited_once_with(event, {})
        mock_redis.setex.assert_awaited_once()

    async def test_callback_within_limit_answer_called(self, mock_redis, mock_handler):
        """
        CallbackQuery в пределах лимита → handler НЕ вызывается,
        вызывается event.answer() с предупреждением.
        """
        event = self._make_callback_event()

        middleware = ThrottlingMiddleware(mock_redis)
        middleware.rate_limits = {type(event): 0.5}
        mock_redis.get.return_value = str(time.time())

        await middleware(mock_handler, event, {})

        mock_handler.assert_not_awaited()
        event.answer.assert_awaited_once_with("⏳ Слишком часто!", show_alert=False)

    async def test_different_user_ids_isolated(self, mock_redis, mock_handler):
        """Разные пользователи не влияют друг на друга."""
        middleware1 = ThrottlingMiddleware(mock_redis)
        event1 = self._make_event(user_id=12345)
        middleware1.rate_limits = {type(event1): 1.0}

        mock_redis.get.return_value = None
        await middleware1(mock_handler, event1, {})

        middleware2 = ThrottlingMiddleware(mock_redis)
        event2 = self._make_event(user_id=99999)
        middleware2.rate_limits = {type(event2): 1.0}

        mock_redis.get.return_value = None
        await middleware2(mock_handler, event2, {})

        assert mock_redis.get.call_count == 2
        keys = [call[0][0] for call in mock_redis.get.call_args_list]
        assert "throttle:12345" in keys
        assert "throttle:99999" in keys
        assert keys[0] != keys[1]  # разные ключи
