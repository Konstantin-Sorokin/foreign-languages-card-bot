from unittest.mock import AsyncMock

from bot.utils.redis_keys import RedisKeys


class TestUserService:
    """Тесты для UserService."""

    async def test_get_user_id_from_cache(self, user_service, mock_redis):
        """Должен вернуть ID пользователя из кэша Redis, не обращаясь к API."""
        telegram_id = 123
        cached_user_id = "42"
        mock_redis.get.return_value = cached_user_id

        result = await user_service.get_user_id(telegram_id)

        assert result == 42
        mock_redis.get.assert_awaited_once_with(RedisKeys.user_id(telegram_id))
        # Убеждаемся, что _request не вызывался (не ходили в API)
        user_service._request = AsyncMock()
        await user_service.get_user_id(telegram_id)
        user_service._request.assert_not_called()

    async def test_get_user_id_no_cache(self, user_service, mock_redis):
        """Должен сходить в API и закэшировать результат, если кэш пуст."""
        telegram_id = 123
        user_data = {"id": 42, "telegram_id": 123}
        mock_redis.get.return_value = None  # кэш пуст
        user_service._request = AsyncMock(return_value=user_data)

        result = await user_service.get_user_id(telegram_id)

        assert result == 42
        mock_redis.get.assert_awaited_once_with(RedisKeys.user_id(telegram_id))
        user_service._request.assert_awaited_once_with(
            method="POST",
            endpoint="users/",
            json={"telegram_id": telegram_id},
        )
        mock_redis.setex.assert_awaited_once_with(
            RedisKeys.user_id(telegram_id),
            7 * 24 * 60 * 60,
            "42",
        )

    async def test_get_or_create_user(self, user_service, mock_redis):
        """Должен вызвать _request с правильными параметрами и вернуть словарь пользователя."""
        telegram_id = 123
        expected_data = {"id": 42, "telegram_id": 123}
        user_service._request = AsyncMock(return_value=expected_data)

        result = await user_service._get_or_create_user(telegram_id)

        assert result == expected_data
        user_service._request.assert_awaited_once_with(
            method="POST",
            endpoint="users/",
            json={"telegram_id": telegram_id},
        )

    async def test_get_user_from_redis(self, user_service, mock_redis):
        """Должен вызвать redis.get с правильным ключом."""
        telegram_id = 123
        mock_redis.get.return_value = "42"

        result = await user_service._get_user_from_redis(telegram_id)

        assert result == "42"
        mock_redis.get.assert_awaited_once_with(RedisKeys.user_id(telegram_id))

    async def test_get_user_from_redis_none(self, user_service, mock_redis):
        """Должен вернуть None, если в кэше ничего нет."""
        mock_redis.get.return_value = None

        result = await user_service._get_user_from_redis(123)

        assert result is None

    async def test_set_user_to_redis(self, user_service, mock_redis):
        """Должен сохранить ID пользователя в Redis с TTL 7 дней."""
        telegram_id = 123
        user_id = 42

        await user_service._set_user_to_redis(telegram_id, user_id)

        mock_redis.setex.assert_awaited_once_with(
            RedisKeys.user_id(telegram_id),
            7 * 24 * 60 * 60,
            "42",
        )
