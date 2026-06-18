from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.constants import LearningKbCallbacks, LearningKbTexts


def build_pack_selection_kb(packs: list[dict]) -> InlineKeyboardMarkup:
    """
    Создаёт клавиатуру для выбора пака глаголов.

    Для каждого пака создаётся кнопка с его названием и callback_data: pack_{id}.
    В конце добавляется кнопка "Случайные глаголы" для перемешивания всех паков.
    """
    builder = InlineKeyboardBuilder()
    all_packs = []
    for pack in packs:
        pack_id = int(pack.get("id"))
        all_packs.append(pack_id)
        builder.button(text=pack.get("name"), callback_data=f"pack_{pack_id}")

    builder.button(
        text=LearningKbTexts.RANDOM_IVC, callback_data=LearningKbCallbacks.RANDOM_IVC
    )
    builder.adjust(2)

    return builder.as_markup()
