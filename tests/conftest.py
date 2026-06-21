from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from redis.asyncio import Redis

from bot.services import CardService, PackService, ProgressService, UserService
from bot.services.base import BaseService


@pytest.fixture
def mock_redis() -> MagicMock:
    """Мок для Redis с async-методами."""
    mock = MagicMock(spec=Redis)

    # Основные async-методы, используемые в сервисах
    mock.get = AsyncMock()
    mock.set = AsyncMock()
    mock.setex = AsyncMock()
    mock.delete = AsyncMock()
    mock.lpop = AsyncMock()
    mock.rpush = AsyncMock()
    mock.lrange = AsyncMock()
    mock.exists = AsyncMock()
    mock.expire = AsyncMock()
    mock.pipeline = MagicMock()

    # Мок для pipeline
    # rpush — синхронный (только буферизирует команду, не делает запрос)
    # expire/execute — асинхронные
    pipe_mock = MagicMock()
    pipe_mock.rpush = MagicMock()
    pipe_mock.delete = AsyncMock()
    pipe_mock.expire = AsyncMock()
    pipe_mock.execute = AsyncMock()
    pipe_mock.__aenter__ = AsyncMock()
    pipe_mock.__aexit__ = AsyncMock()
    mock.pipeline.return_value = pipe_mock

    return mock


@pytest.fixture
def mock_http_session():
    """Мок для aiohttp.ClientSession."""
    with patch("aiohttp.ClientSession") as mock:
        session_instance = MagicMock()
        mock.return_value = session_instance
        yield mock


@pytest.fixture
def base_service(mock_redis) -> BaseService:
    """BaseService с замоканным Redis (без HTTP-запроса)."""
    service = BaseService(redis_client=mock_redis)
    return service


@pytest.fixture
def user_service(mock_redis) -> UserService:
    """UserService с замоканным Redis."""
    return UserService(redis_client=mock_redis)


@pytest.fixture
def card_service(mock_redis) -> CardService:
    """CardService с замоканным Redis."""
    return CardService(redis_client=mock_redis)


@pytest.fixture
def pack_service(mock_redis) -> PackService:
    """PackService с замоканным Redis."""
    return PackService(redis_client=mock_redis)


@pytest.fixture
def progress_service(mock_redis) -> ProgressService:
    """ProgressService с замоканным Redis."""
    return ProgressService(redis_client=mock_redis)
