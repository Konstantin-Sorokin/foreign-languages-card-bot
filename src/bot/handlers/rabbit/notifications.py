from aiogram import Bot

from bot.schemas.rabbit import NotificationMessage


async def handle_notification(
    data: dict,
):
    """Route incoming notification to the appropriate handler."""

    message = NotificationMessage.model_validate(data)

    match message.event:
        case "learning_reminder":
            await send_learning_reminder(message)

        case _:
            pass


async def send_learning_reminder(
    message: NotificationMessage,
):
    """Send a push notification reminding the user to review cards."""

    bot: Bot = ...

    await bot.send_message(
        chat_id=message.telegram_id,
        text="📚 Время повторить карточки!",
    )
