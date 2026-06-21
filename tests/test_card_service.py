import json
from unittest.mock import AsyncMock

from bot.utils.redis_keys import RedisKeys


class TestCardService:
    async def test_initialize_learning_queue_with_cards(self, card_service, mock_redis):
        """Должен очистить очередь и загрузить карточки, если API вернул данные."""
        cards = [
            {"id": 1, "original": "hello", "translation": "привет"},
            {"id": 2, "original": "world", "translation": "мир"},
        ]
        card_service._request = AsyncMock(return_value=cards)

        result = await card_service.initialize_learning_queue(
            telegram_id=123, user_id=1
        )

        assert result is True
        queue_key = RedisKeys.user_cards(123)
        mock_redis.delete.assert_awaited_once_with(queue_key)
        pipe = mock_redis.pipeline.return_value
        assert pipe.rpush.call_count == len(cards)

    async def test_initialize_learning_queue_empty(self, card_service, mock_redis):
        """Должен вернуть False, если API вернул пустой список."""
        card_service._request = AsyncMock(return_value=[])

        result = await card_service.initialize_learning_queue(
            telegram_id=123, user_id=1
        )

        assert result is False
        mock_redis.delete.assert_not_called()
        mock_redis.rpush.assert_not_called()

    async def test_get_next_card_from_queue_exists(self, card_service, mock_redis):
        """Должен вернуть карточку из очереди."""
        card = {"id": 1, "original": "hello", "translation": "привет"}
        mock_redis.lpop.return_value = json.dumps(card, ensure_ascii=False)

        result = await card_service.get_next_card_from_queue(telegram_id=123)

        assert result == card
        mock_redis.lpop.assert_awaited_once_with(RedisKeys.user_cards(123))

    async def test_get_next_card_from_queue_empty(self, card_service, mock_redis):
        """Должен вернуть None, если очередь пуста."""
        mock_redis.lpop.return_value = None

        result = await card_service.get_next_card_from_queue(telegram_id=123)

        assert result is None

    async def test_add_card_to_the_end_queue(self, card_service, mock_redis):
        """Должен добавить карточку в конец очереди."""
        card = {"id": 1, "original": "hello", "translation": "привет"}

        await card_service.add_card_to_the_end_queue(telegram_id=123, card=card)

        mock_redis.rpush.assert_awaited_once_with(
            RedisKeys.user_cards(123), json.dumps(card, ensure_ascii=False)
        )

    async def test_add_cards_to_queue(self, card_service, mock_redis):
        """Должен добавить список карточек через pipeline и установить TTL."""
        cards = [
            {"id": 1, "original": "hello", "translation": "привет"},
            {"id": 2, "original": "world", "translation": "мир"},
        ]
        pipe = mock_redis.pipeline.return_value

        await card_service.add_cards_to_queue(telegram_id=123, cards=cards)

        mock_redis.pipeline.assert_called_once()
        assert pipe.rpush.call_count == len(cards)
        pipe.rpush.assert_any_call(
            RedisKeys.user_cards(123), json.dumps(cards[0], ensure_ascii=False)
        )
        pipe.rpush.assert_any_call(
            RedisKeys.user_cards(123), json.dumps(cards[1], ensure_ascii=False)
        )
        pipe.expire.assert_awaited_once_with(RedisKeys.user_cards(123), 3600)
        pipe.execute.assert_awaited_once()
