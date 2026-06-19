import pytest

from bot.utils.redis_keys import RedisKeys


class TestRedisKeys:
    """Тесты для статических методов RedisKeys — проверка формата ключей."""

    @pytest.mark.parametrize(
        ("method", "args", "expected"),
        [
            (RedisKeys.user_id, (123,), "user:123:id"),
            (RedisKeys.user_id, (999999,), "user:999999:id"),
            (RedisKeys.user_id, (0,), "user:0:id"),
            (RedisKeys.user_cards, (123,), "user:123:cards"),
            (RedisKeys.user_cards, (42,), "user:42:cards"),
            (RedisKeys.user_verbs, (123,), "user:123:verbs"),
            (RedisKeys.user_verbs, (5,), "user:5:verbs"),
            (RedisKeys.pack_verbs, (1,), "pack:1:verbs_cache"),
            (RedisKeys.pack_verbs, (100500,), "pack:100500:verbs_cache"),
            (RedisKeys.packs_list, (), "packs:list"),
        ],
    )
    def test_redis_keys(self, method, args, expected):
        assert method(*args) == expected
