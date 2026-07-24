from aiogram import Bot

from bot.schemas.rabbit import NotificationMessage


class NotificationHandler:
    def __init__(
        self,
        bot: Bot,
    ):
        self.bot = bot

    async def handle(
        self,
        message: NotificationMessage,
    ):
        """Process a notification and send the appropriate message to the user."""

        match message.event:
            case "learning_reminder":
                await self.bot.send_message(
                    chat_id=message.telegram_id,
                    text="📚 У вас есть карточки для повторения",
                )
