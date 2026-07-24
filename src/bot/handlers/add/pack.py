from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from bot.keyboards.add import get_addable_packs_kb, get_packs_kb, get_set_actions_kb
from bot.resources import AppResources
from bot.utils.callbacks import AddCallbacks, PackAction, PackCallback
from bot.utils.enums import PackKind
from bot.utils.formatters import render_pack_text

router = Router(name=__name__)


@router.callback_query(F.data == AddCallbacks.PACK)
async def show_packs(
    callback: CallbackQuery,
    resources: AppResources,
    user_id: int,
):
    """Open the pack selection menu."""
    await render_packs(
        callback=callback,
        pack_id=None,
        user_id=user_id,
        resources=resources,
    )


@router.callback_query(PackCallback.filter(F.action == PackAction.OPEN))
async def open_pack(
    callback: CallbackQuery,
    callback_data: PackCallback,
    resources: AppResources,
    user_id: int,
):
    """Open a specific pack and show its contents."""
    await render_packs(
        callback=callback,
        pack_id=callback_data.pack_id,
        user_id=user_id,
        resources=resources,
        added=callback_data.added,
    )


@router.callback_query(PackCallback.filter(F.action == PackAction.ADD))
async def add_pack(
    callback: CallbackQuery,
    callback_data: PackCallback,
    resources: AppResources,
    user_id: int,
):
    """Subscribe user to the selected pack."""
    pack_id = callback_data.pack_id
    if pack_id is None:
        return

    await resources.pack_service.add_pack(
        user_id=user_id,
        pack_id=pack_id,
    )

    parent_id = resources.pack_service.get_parent_id(pack_id)

    await render_packs(
        callback=callback,
        pack_id=parent_id,
        user_id=user_id,
        resources=resources,
    )


@router.callback_query(PackCallback.filter(F.action == PackAction.BACK))
async def back(
    callback: CallbackQuery,
    callback_data: PackCallback,
    resources: AppResources,
    user_id: int,
):
    """Navigate back to the parent pack."""
    await render_packs(
        callback=callback,
        pack_id=callback_data.pack_id,
        user_id=user_id,
        resources=resources,
    )


async def render_packs(
    callback: CallbackQuery,
    pack_id: int | None,
    user_id: int,
    resources: AppResources,
    added: bool | None = None,
):
    """Render the pack browser with breadcrumbs and action buttons."""
    if not isinstance(callback.message, Message):
        return

    response = await resources.pack_service.get_packs(
        user_id=user_id,
        pack_id=pack_id,
    )

    breadcrumbs = resources.pack_service.get_breadcrumbs(pack_id)

    current_pack = breadcrumbs[-1] if breadcrumbs else None

    back_pack_id = current_pack.parent_id if current_pack else None

    if current_pack and current_pack.kind == PackKind.SET:
        if added is None:
            return

        kb = get_set_actions_kb(
            pack_id=current_pack.id,
            back_pack_id=current_pack.parent_id,
            added=added,
        )

    elif response.packs and response.packs[0].kind == PackKind.SET:
        kb = get_addable_packs_kb(
            packs=response.packs,
            back_pack_id=back_pack_id,
        )

    else:
        kb = get_packs_kb(
            packs=response.packs,
            show_back=current_pack is not None,
            back_pack_id=back_pack_id,
        )

    text = render_pack_text(
        breadcrumbs=breadcrumbs,
    )

    await callback.message.edit_text(
        text=text,
        reply_markup=kb,
    )
