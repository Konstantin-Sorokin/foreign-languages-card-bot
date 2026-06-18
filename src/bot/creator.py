import redis.asyncio as redis
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from bot.handlers import router
from bot.middlewares import ThrottlingMiddleware
from bot.utils import settings


def get_redis_client() -> redis.Redis:
    """Создаёт и возвращает клиент Redis с декодированием ответов."""
    return redis.Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        db=settings.redis.db,
        decode_responses=True,
    )


def create_dispatcher() -> Dispatcher:
    """
    Создаёт и настраивает Dispatcher.

    - Инициализирует Redis storage для FSM
    - Регистрирует ThrottlingMiddleware для сообщений и callback-запросов
    - Подключает корневой роутер со всеми хэндлерами
    """
    redis_client = get_redis_client()
    fsm_storage = RedisStorage(redis=redis_client)

    dp = Dispatcher(storage=fsm_storage)
    dp.workflow_data["redis"] = redis_client

    throttling = ThrottlingMiddleware(redis=redis_client)
    dp.message.middleware.register(throttling)
    dp.callback_query.middleware.register(throttling)

    dp.include_router(router)
    return dp


def create_bot() -> Bot:
    """
    Создаёт экземпляр бота с HTML-парсингом по умолчанию.

    Если указан PROXY_URL, используется сессия с прокси (aiohttp-socks).
    """
    if settings.proxy_url:
        session = AiohttpSession(proxy=settings.proxy_url)
        bot = Bot(
            token=settings.token,
            session=session,
            default=DefaultBotProperties(
                parse_mode=ParseMode.HTML,
            ),
        )
    else:
        bot = Bot(
            token=settings.token,
            default=DefaultBotProperties(
                parse_mode=ParseMode.HTML,
            ),
        )

    return bot
