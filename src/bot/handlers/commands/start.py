from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.keyboards.start import get_start_kb
from bot.texts.messages import START_MESSAGE
from bot.utils.constants import START_COMMAND

router = Router(name=__name__)


@router.message(Command(START_COMMAND))
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    """Show the main menu."""
    await state.clear()

    await message.answer(
        text=START_MESSAGE,
        reply_markup=get_start_kb(),
    )
