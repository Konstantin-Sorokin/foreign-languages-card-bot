from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.constants import (
    AddCardCallbacks,
    AddCardTexts,
)


def build_confirm_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text=AddCardTexts.CONFIRM, callback_data=AddCardCallbacks.CONFIRM)
    builder.button(text=AddCardTexts.CANCEL, callback_data=AddCardCallbacks.CANCEL)

    builder.adjust(2, 1)
    return builder.as_markup()
