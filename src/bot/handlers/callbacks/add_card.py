from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from redis.asyncio import Redis

from bot.keyboards.start_kb import get_start_kb
from bot.services import ProgressService, UserService
from bot.states import AddCardStates
from bot.utils.constants import AddCardCallbacks, Texts

router = Router()


@router.callback_query(F.data == AddCardCallbacks.ADD_EXAMPLE)
async def cb_add_example(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик нажатия кнопки 'Добавить пример' при создании карточки.
    Устанавливает состояние ожидания ввода примера на языке оригинала.
    """
    await callback.message.edit_text(Texts.INPUT_EXAMPLE_MSG)
    await state.set_state(AddCardStates.input_example)
    await callback.answer()


@router.callback_query(
    F.data.in_(
        [
            AddCardCallbacks.CONFIRM_WO_EXAMPLE,
            AddCardCallbacks.CONFIRM_W_EXAMPLE,
        ]
    )
)
async def cb_confirm_card(
    callback: CallbackQuery, state: FSMContext, redis: Redis
) -> None:
    """
    Обработчик, который собирает все нужные данные для сохранения карточки.
    Полученные данные отправляются в progress_service, который работает с API для сохранения карточки в БД.
    После этого удаляется состояние и все данные. Вызывается стартовая клавиатура.
    """
    progress_service = ProgressService(redis_client=redis)
    user_service = UserService(redis_client=redis)
    user_id = await user_service.get_user_id(callback.from_user.id)
    state_data = await state.get_data()

    await progress_service.create_progress(
        user_id=user_id,
        original=state_data["original"],
        translation=state_data["translation"],
        example=state_data.get("example", ""),
        example_translation=state_data.get("example_translation", ""),
    )

    await state.clear()
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(Texts.SUCCESS_MSG, reply_markup=get_start_kb())


@router.callback_query(F.data == AddCardCallbacks.CANCEL)
async def cb_cancel(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик для отмены добавления карточки.
    Удаляет состояние и все данные. Вызывает стартовую клавиатуру.
    """
    await state.clear()
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(Texts.CANCEL_MSG, reply_markup=get_start_kb())
