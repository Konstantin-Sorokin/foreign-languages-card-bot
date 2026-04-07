from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.keyboards.learn_kbs import get_next_tc_kb
from bot.services import CardService, ProgressService, UserService
from bot.states import LearningStates
from bot.utils.constants import CardActionCallbacks, CardActionTexts

router = Router()


@router.callback_query(
    F.data == CardActionCallbacks.KNOW,
    LearningStates.evaluating,
)
async def evaluating_know_handler(callback: CallbackQuery, state: FSMContext):
    await _process_evaluation(
        callback=callback,
        state=state,
        success=True,
        message=CardActionTexts.KNOW_MESSAGE,
    )


@router.callback_query(
    F.data == CardActionCallbacks.DONT_KNOW,
    LearningStates.evaluating,
)
async def evaluating_dont_know_handler(callback: CallbackQuery, state: FSMContext):
    await _process_evaluation(
        callback=callback,
        state=state,
        success=False,
        message=CardActionTexts.DONT_KNOW_MESSAGE,
    )


async def _process_evaluation(
    callback: CallbackQuery,
    state: FSMContext,
    success: bool,
    message: str,
):
    await callback.answer()

    data = await state.get_data()
    card = data.get("current_card")
    card_id = card.get("id")
    user_id = await UserService(callback.bot.redis).get_user_id(callback.from_user.id)

    await ProgressService(callback.bot.redis).update_progress(
        user_id=user_id,
        card_id=card_id,
        success=success,
    )

    if not success:
        await CardService(callback.bot.redis).add_card_to_the_end_queue(
            callback.from_user.id, card
        )

    await state.clear()
    await state.set_state(LearningStates.selecting_type)
    await callback.message.edit_text(text=message, reply_markup=get_next_tc_kb())
