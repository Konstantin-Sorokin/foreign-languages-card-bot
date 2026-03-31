from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.utils.constants import StartKbTexts


def get_start_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text=StartKbTexts.LEARNING)
    builder.button(text=StartKbTexts.ADD_CARD)

    builder.adjust(2)
    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False,
    )
