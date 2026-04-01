import redis.asyncio as redis
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode

from bot.handlers import router
from bot.utils import settings


def create_dispatcher() -> Dispatcher:
    dp = Dispatcher()
    dp.include_router(router)
    dp.redis = redis.Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        db=settings.redis.db,
    )

    return dp


def create_bot() -> Bot:
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
