from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.texts.buttons import StartButtons


def get_start_kb() -> ReplyKeyboardMarkup:
    """Main menu keyboard."""
    builder = ReplyKeyboardBuilder()

    builder.button(text=StartButtons.LEARNING)
    builder.button(text=StartButtons.ADD)

    builder.adjust(2)

    return builder.as_markup(
        resize_keyboard=True,
    )
