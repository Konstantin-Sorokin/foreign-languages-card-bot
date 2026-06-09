from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from redis.asyncio import Redis

from bot.keyboards.learn_kbs import (
    get_evaluation_kb,
    get_next_tc_kb,
    get_show_answer_kb,
)
from bot.keyboards.start_kb import get_start_kb
from bot.services import CardService, ProgressService, UserService
from bot.states import LearningStates
from bot.utils.constants import (
    CardActionCallbacks,
    LearningKbCallbacks,
    Texts,
)

router = Router()


@router.callback_query(
    F.data == LearningKbCallbacks.TRANSLATION_CARDS,
    LearningStates.choosing_mode,
)
async def cb_init_cards_learning(
    callback: CallbackQuery, state: FSMContext, redis: Redis
):
    """
    Запускает сессию обучения

    - Формирует очередь карточек для пользователя в Redis с помощью initialize_learning_queue
    - Берет первую карточку с помощью метода lpop и сохраняет ее в FSM State
    - Переключает состояние в tc_checking и показывает лицевую сторону карточки
    - При отсутствии карточек, предлагает создать новые
    """
    await callback.answer()
    await state.set_state(LearningStates.tc_checking)

    user_id = await UserService(redis).get_user_id(callback.from_user.id)
    await CardService(redis).initialize_learning_queue(callback.from_user.id, user_id)
    card = await CardService(redis).get_next_card_from_queue(callback.from_user.id)

    if not card:
        await callback.message.delete()
        await callback.message.answer(
            text=Texts.NO_CARDS,
            reply_markup=get_start_kb(),
        )
        return

    await state.update_data(current_card=card)
    await _show_original(callback, card)


@router.callback_query(
    F.data == LearningKbCallbacks.NEXT_CARD,
    LearningStates.tc_thinking,
)
async def cb_load_next_card(callback: CallbackQuery, state: FSMContext, redis: Redis):
    """
    Загружает следующую карточку для обучения

    - Берет первую карточку из очереди пользователя с помощью метода lpop и сохраняет ее в FSM State
    - Переключает состояние в tc_checking и показывает лицевую сторону карточки
    - При отсутствии карточек, проверяет на доступность новых в БД
    - При отсутствии в БД предлагает создать новые
    """
    await callback.answer()
    await state.set_state(LearningStates.tc_checking)

    card = await CardService(redis).get_next_card_from_queue(callback.from_user.id)

    if not card:
        user_id = await UserService(redis).get_user_id(callback.from_user.id)
        if not await CardService(redis).initialize_learning_queue(
            callback.from_user.id, user_id
        ):
            await callback.message.delete()
            await callback.message.answer(
                text=Texts.NO_CARDS,
                reply_markup=get_start_kb(),
            )
            return
        card = await CardService(redis).get_next_card_from_queue(callback.from_user.id)

    await state.update_data(current_card=card)
    await _show_original(callback, card)


@router.callback_query(
    F.data == CardActionCallbacks.SHOW_ANSWER,
    LearningStates.tc_checking,
)
async def cb_show_translate_and_evaluation(callback: CallbackQuery, state: FSMContext):
    """
    Отображает обратную сторону карточки и предлагает оценить знания

    - Берет текущую карту из FSM State и переключает состояние в tc_waiting_evaluation
    - Отображает всю доступную информацию по карточке
    - Предлагает оценить свои знания карточки - ЗНАЮ или НЕ ЗНАЮ
    """
    await callback.answer()
    await state.set_state(LearningStates.tc_waiting_evaluation)

    state_data = await state.get_data()
    card = state_data.get("current_card")

    await _show_all(callback, card)


@router.callback_query(
    F.data == CardActionCallbacks.KNOW,
    LearningStates.tc_waiting_evaluation,
)
async def cb_evaluate_know(callback: CallbackQuery, state: FSMContext, redis: Redis):
    """
    Обрабатывает нажатие кнопки знаю с помощью _process_evaluation
    """
    await _process_evaluation(
        callback=callback,
        state=state,
        success=True,
        message=Texts.KNOW,
        redis=redis,
    )


@router.callback_query(
    F.data == CardActionCallbacks.DONT_KNOW,
    LearningStates.tc_waiting_evaluation,
)
async def cb_evaluate_dont_know(
    callback: CallbackQuery, state: FSMContext, redis: Redis
):
    """
    Обрабатывает нажатие кнопки знаю с помощью _process_evaluation
    """
    await _process_evaluation(
        callback=callback,
        state=state,
        success=False,
        message=Texts.DONT_KNOW,
        redis=redis,
    )


async def _show_original(callback: CallbackQuery, card: dict):
    """Показывает оригинал слова и пример (если есть)."""
    original = card["original"]
    example = card.get("example", "")

    text = f"🇬🇧 <b>{original}</b>"
    if example:
        text += f"\n\n<i>{example}</i>"

    await callback.message.edit_text(
        text=text,
        reply_markup=get_show_answer_kb(),
    )


async def _show_all(callback: CallbackQuery, card: dict):
    """Показывает полную информацию: слово, перевод и пример с переводом(если есть)."""
    original = card["original"]
    translation = card["translation"]
    example = card.get("example", "")
    example_trans = card.get("example_translation", "")

    text = f"🇬🇧 <b>{original}</b>\n🇷🇺 <b>{translation}</b>"

    if example or example_trans:
        text += "\n\n"
        if example:
            text += f"<i>{example}</i>\n"
        if example_trans:
            text += f"<i>{example_trans}</i>"

    await callback.message.edit_text(
        text=text,
        reply_markup=get_evaluation_kb(),
    )


async def _process_evaluation(
    callback: CallbackQuery,
    state: FSMContext,
    success: bool,
    message: str,
    redis: Redis,
):
    """
    Обрабатывает переданную информацию от обработчиков кнопок ЗНАЮ / НЕ ЗНАЮ

    - Обновляет данные карточки в БД в зависимости от ответа(success)
    - Если пользователь не знает карточку success == False, то карточка переходит в конец очереди пользователя
    для повторного показа
    - Переключает состояние в tc_thinking и предлагает пользователю выбрать следующую карточку
    """
    await callback.answer()

    data = await state.get_data()
    card = data.get("current_card")
    card_id = card.get("id")
    user_id = await UserService(redis).get_user_id(callback.from_user.id)

    await ProgressService(redis).update_progress(
        user_id=user_id,
        card_id=card_id,
        success=success,
    )

    if not success:
        await CardService(redis).add_card_to_the_end_queue(callback.from_user.id, card)

    await state.clear()
    await state.set_state(LearningStates.tc_thinking)
    await callback.message.edit_text(text=message, reply_markup=get_next_tc_kb())
