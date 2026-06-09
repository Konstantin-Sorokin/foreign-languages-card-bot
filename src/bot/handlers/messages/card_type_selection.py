from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.keyboards.learn_kbs import get_learning_choice_kb
from bot.states import LearningStates
from bot.utils.constants import StartKbTexts, Texts

router = Router()


@router.message(F.text == StartKbTexts.LEARNING)
async def msg_card_type_selection(
    message: Message,
    state: FSMContext,
):
    """
    Начинает обучение - предлагает выбрать тип карточек и
    переключает состояние обучения в choosing_mode.
    """
    await state.set_state(LearningStates.choosing_mode)
    await message.answer(
        Texts.SELECT_TYPE_LEARNING,
        reply_markup=get_learning_choice_kb(),
    )
