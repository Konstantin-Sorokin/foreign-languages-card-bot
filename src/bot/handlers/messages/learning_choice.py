from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.keyboards.learn_kbs import get_learning_choice_kb
from bot.states import LearningStates
from bot.utils.constants import StartKbTexts

router = Router()


@router.message(F.text == StartKbTexts.LEARNING)
async def learning_choice_handler(
    message: Message,
    state: FSMContext,
):
    await state.set_state(LearningStates.selecting_type)
    await message.answer(
        "Выберите тип обучения:",
        reply_markup=get_learning_choice_kb(),
    )
