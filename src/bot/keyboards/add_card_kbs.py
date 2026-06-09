from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.constants import (
    AddCardCallbacks,
    AddCardTexts,
)


def build_confirm_keyboard(added_example=False) -> InlineKeyboardMarkup:
    """
    Функция для создания клавиатуры для двух ситуаций:

    1. Добавление карточки в момент выбора - сохранить / отменить / добавить пример
    2. Добавление карточки в момент выбора - сохранить(уже с примером) / отменить

    Параметр added_example по умолчанию False и это значит, что клавиатура
    создается на моменте 1 выбора.
    """

    builder = InlineKeyboardBuilder()

    if added_example:
        builder.button(
            text=AddCardTexts.CONFIRM_W_EXAMPLE,
            callback_data=AddCardCallbacks.CONFIRM_W_EXAMPLE,
        )
    else:
        builder.button(
            text=AddCardTexts.CONFIRM_WO_EXAMPLE,
            callback_data=AddCardCallbacks.CONFIRM_WO_EXAMPLE,
        )

        builder.button(
            text=AddCardTexts.ADD_EXAMPLE,
            callback_data=AddCardCallbacks.ADD_EXAMPLE,
        )

    builder.button(text=AddCardTexts.CANCEL, callback_data=AddCardCallbacks.CANCEL)

    builder.adjust(1)
    return builder.as_markup()
