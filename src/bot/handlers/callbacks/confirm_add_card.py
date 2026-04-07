from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.keyboards.start_kb import get_start_kb
from bot.services import ProgressService, UserService
from bot.utils.constants import AddCardCallbacks, AddCardTexts

router = Router()


@router.callback_query(F.data == AddCardCallbacks.CONFIRM)
async def confirm_handler(callback: CallbackQuery, state: FSMContext):
    progress_service = ProgressService(redis_client=callback.bot.redis)
    user_service = UserService(redis_client=callback.bot.redis)
    user_id = await user_service.get_user_id(callback.from_user.id)
    data = await state.get_data()

    await progress_service.create_progress(
        user_id=user_id,
        original=data["original"],
        translation=data["translation"],
    )
    await state.clear()
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(
        AddCardTexts.SUCCESS_MESSAGE, reply_markup=get_start_kb()
    )


@router.callback_query(F.data == AddCardCallbacks.CANCEL)
async def cancel_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(
        AddCardTexts.CANCEL_MESSAGE, reply_markup=get_start_kb()
    )
