import aio_pika
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from redis import asyncio as redis

from bot.api.cards import CardApi
from bot.api.learning import LearningApi
from bot.api.packs import PackApi
from bot.api.users import UserApi
from bot.cache.cache_service import CacheService
from bot.core.config import settings
from bot.handlers import router
from bot.middlewares import ThrottlingMiddleware
from bot.middlewares.user import UserMiddleware
from bot.rabbit.consumer import NotificationConsumer
from bot.rabbit.handlers import NotificationHandler
from bot.resources import AppResources
from bot.services.card import CardService
from bot.services.learning import LearningService
from bot.services.pack import PackService
from bot.services.user import UserService
from bot.storage.storage import Storage
from bot.utils.bot_commands import COMMANDS


def create_bot() -> Bot:
    """Create and configure the bot instance."""
    if settings.proxy_url:
        session = AiohttpSession(proxy=settings.proxy_url)

        return Bot(
            token=settings.token,
            session=session,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )

    return Bot(
        token=settings.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )


async def create_resources() -> AppResources:
    """Initialize all application dependencies."""
    bot = create_bot()

    redis_client = redis.Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        db=settings.redis.db,
        decode_responses=True,
    )
    cache = CacheService(redis_client)

    http = aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=30),
    )

    storage = Storage()

    card_api = CardApi(http, settings.api_url)
    learning_api = LearningApi(http, settings.api_url)
    pack_api = PackApi(http, settings.api_url)
    user_api = UserApi(http, settings.api_url)

    card_service = CardService(card_api=card_api)
    learning_service = LearningService(
        cache=cache, learning_api=learning_api, storage=storage
    )
    pack_service = PackService(
        pack_api=pack_api, learning_api=learning_api, storage=storage
    )
    user_service = UserService(user_api=user_api, cache=cache)

    await pack_service.verbs_by_group()
    await pack_service.load_packs()

    rabbit_connection = await aio_pika.connect_robust(url=settings.rabbit.url)

    rabbit_channel = await rabbit_connection.channel()

    notification_handler = NotificationHandler(
        bot=bot,
    )

    notification_consumer = NotificationConsumer(
        connection=rabbit_connection,
        handler=notification_handler,
    )

    return AppResources(
        bot=bot,
        redis=redis_client,
        http=http,
        rabbit_connection=rabbit_connection,
        rabbit_channel=rabbit_channel,
        notification_consumer=notification_consumer,
        card_service=card_service,
        learning_service=learning_service,
        pack_service=pack_service,
        user_service=user_service,
    )


def create_dispatcher(resources: AppResources) -> Dispatcher:
    """Create and configure the dispatcher with middleware and routers."""
    dp = Dispatcher(
        storage=RedisStorage(redis=resources.redis),
    )

    dp.workflow_data["resources"] = resources

    dp.update.middleware(ThrottlingMiddleware(redis=resources.redis))
    dp.update.middleware(UserMiddleware(user_service=resources.user_service))

    dp.include_router(router)

    return dp


async def setup_bot(resources: AppResources) -> None:
    """Register bot commands."""
    await resources.bot.set_my_commands(COMMANDS)


async def shutdown_resources(resources: AppResources) -> None:
    """Gracefully close all connections and resources."""
    await resources.http.close()
    await resources.redis.aclose()

    await resources.rabbit_connection.close()

    await resources.bot.close()
