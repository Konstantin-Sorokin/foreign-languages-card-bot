from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.keyboards.learning import get_learning_menu_kb
from bot.texts.buttons import StartButtons
from bot.texts.messages import LEARNING_MENU

router = Router()


@router.message(F.text == StartButtons.LEARNING)
async def open_learning_menu(
    message: Message,
    state: FSMContext,
):
    """Open the learning menu."""

    await state.clear()

    await message.answer(
        text=LEARNING_MENU,
        reply_markup=get_learning_menu_kb(),
    )
