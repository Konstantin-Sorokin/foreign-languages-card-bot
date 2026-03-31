from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.keyboards.start_kb import get_start_kb
from bot.utils.constants import HELP_COMMAND, START_COMMAND

router = Router(name=__name__)


@router.message(Command(START_COMMAND))
async def start_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Привет! 👋\n\nВыберите действие:",
        reply_markup=get_start_kb(),
    )


@router.message(Command(HELP_COMMAND))
async def help_handler(message: types.Message):
    await message.answer("помощник")
