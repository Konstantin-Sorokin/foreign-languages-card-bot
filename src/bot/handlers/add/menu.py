from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.keyboards.add import get_add_menu_kb
from bot.texts.buttons import StartButtons
from bot.texts.messages import ADD_MENU

router = Router(name=__name__)


@router.message(F.text == StartButtons.ADD)
async def open_add_menu(
    message: Message,
    state: FSMContext,
) -> None:
    """Open the add menu."""

    await state.clear()

    await message.answer(
        text=ADD_MENU,
        reply_markup=get_add_menu_kb(),
    )
