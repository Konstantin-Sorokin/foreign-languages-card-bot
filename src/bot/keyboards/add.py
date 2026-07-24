from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.schemas.pack import PackRead
from bot.texts.buttons import AddButtons, CardButtons, PackButtons
from bot.utils.callbacks import AddCallbacks, CardCallbacks, PackCallback
from bot.utils.enums import PackAction


def get_add_menu_kb() -> InlineKeyboardMarkup:
    """Keyboard for choosing the add method."""
    builder = InlineKeyboardBuilder()

    builder.button(text=AddButtons.CARD, callback_data=AddCallbacks.CARD)
    builder.button(text=AddButtons.PACK, callback_data=AddCallbacks.PACK)
    builder.adjust(2)

    return builder.as_markup()


def get_add_card_confirm_kb(has_example: bool = False) -> InlineKeyboardMarkup:
    """Keyboard for confirming card creation."""
    builder = InlineKeyboardBuilder()

    if has_example:
        builder.button(text=CardButtons.SAVE, callback_data=CardCallbacks.SAVE)
    else:
        builder.button(
            text=CardButtons.SAVE_WITHOUT_EXAMPLE,
            callback_data=CardCallbacks.SAVE_WITHOUT_EXAMPLE,
        )

        builder.button(
            text=CardButtons.ADD_EXAMPLE,
            callback_data=CardCallbacks.ADD_EXAMPLE,
        )

    builder.button(text=CardButtons.CANCEL, callback_data=CardCallbacks.CANCEL)
    builder.adjust(1)

    return builder.as_markup()


def get_packs_kb(
    packs: list[PackRead],
    show_back: bool = False,
    back_pack_id: int | None = None,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for pack in packs:
        if pack.year:
            builder.button(
                text=f"{pack.name} ({pack.year})",
                callback_data=PackCallback(
                    action=PackAction.OPEN,
                    pack_id=pack.id,
                ).pack(),
            )
        else:
            builder.button(
                text=pack.name,
                callback_data=PackCallback(
                    action=PackAction.OPEN,
                    pack_id=pack.id,
                ).pack(),
            )

    if show_back:
        builder.button(
            text=PackButtons.BACK,
            callback_data=PackCallback(
                action=PackAction.BACK, pack_id=back_pack_id
            ).pack(),
        )

    builder.adjust(1)

    return builder.as_markup()


def get_set_actions_kb(
    pack_id: int,
    back_pack_id: int | None,
    added: bool,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if not added:
        builder.button(
            text=PackButtons.ADD,
            callback_data=PackCallback(action=PackAction.ADD, pack_id=pack_id).pack(),
        )

    builder.button(
        text=PackButtons.BACK,
        callback_data=PackCallback(action=PackAction.BACK, pack_id=back_pack_id).pack(),
    )

    builder.adjust(1)

    return builder.as_markup()


def get_addable_packs_kb(
    packs: list[PackRead],
    back_pack_id: int | None,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for pack in packs:
        icon = "🟢" if pack.added else "⚪"

        builder.button(
            text=f"{icon} {pack.name}",
            callback_data=PackCallback(
                action=PackAction.OPEN, pack_id=pack.id, added=pack.added
            ).pack(),
        )

    builder.button(
        text=PackButtons.BACK,
        callback_data=PackCallback(action=PackAction.BACK, pack_id=back_pack_id).pack(),
    )

    builder.adjust(1)

    return builder.as_markup()
