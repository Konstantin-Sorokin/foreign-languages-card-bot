import json
import logging

import aio_pika

from bot.rabbit.handlers import NotificationHandler
from bot.schemas.rabbit import NotificationMessage

logger = logging.getLogger(__name__)


class NotificationConsumer:
    def __init__(
        self,
        connection: aio_pika.RobustConnection,
        handler: NotificationHandler,
    ):
        self.connection = connection
        self.handler = handler

    async def start(self):
        """Start consuming messages from the notifications queue."""

        channel = await self.connection.channel()

        queue = await channel.declare_queue(
            "notifications",
            durable=True,
        )

        logger.info("Rabbit notification consumer started")

        async with queue.iterator() as iterator:
            async for message in iterator:
                async with message.process():
                    data = json.loads(message.body.decode())

                    notification = NotificationMessage.model_validate(data)

                    await self.handler.handle(notification)
