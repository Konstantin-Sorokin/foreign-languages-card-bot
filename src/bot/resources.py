from dataclasses import dataclass

import aio_pika
import aiohttp
from aiogram import Bot
from redis import asyncio as redis

from bot.rabbit.consumer import NotificationConsumer
from bot.services.card import CardService
from bot.services.learning import LearningService
from bot.services.pack import PackService
from bot.services.user import UserService


@dataclass(slots=True)
class AppResources:
    bot: Bot

    redis: redis.Redis
    http: aiohttp.ClientSession

    rabbit_connection: aio_pika.RobustConnection
    rabbit_channel: aio_pika.abc.AbstractChannel
    notification_consumer: NotificationConsumer

    card_service: CardService
    learning_service: LearningService
    pack_service: PackService
    user_service: UserService
