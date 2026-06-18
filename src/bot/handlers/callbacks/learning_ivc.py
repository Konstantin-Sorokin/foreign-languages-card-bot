from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from redis.asyncio import Redis

from bot.keyboards.learn_kbs import get_next_ivc_kb, get_show_answer_kb
from bot.keyboards.packs_kb import build_pack_selection_kb
from bot.services.pack_service import PackService
from bot.states import LearningStates
from bot.utils.constants import (
    CardActionCallbacks,
    LearningKbCallbacks,
    Texts,
)

router = Router()


@router.callback_query(
    F.data == LearningKbCallbacks.IRREGULAR_VERB_CARDS,
    LearningStates.choosing_mode,
)
async def cb_start_pack_selection(
    callback: CallbackQuery, state: FSMContext, redis: Redis
):
    """
    Инициализирует процесс выбора паков для изучения неправильных глаголов.

    - Переключает состояние пользователя в select_pack.
    - Загружает список доступных паков из кэша Redis.
    - Отрисовывает инлайн-клавиатуру для выбора конкретного пака или случайной выборки.
    """
    await callback.answer()
    await state.set_state(LearningStates.select_pack)

    pack_service = PackService(redis_client=redis)
    packs = await pack_service.get_packs()
    await callback.message.edit_text(
        text=Texts.CHANGE_PACK, reply_markup=build_pack_selection_kb(packs)
    )


@router.callback_query(
    (F.data.startswith("pack_")) | (F.data == LearningKbCallbacks.RANDOM_IVC),
    LearningStates.select_pack,
)
async def cb_init_ivc_learning(
    callback: CallbackQuery, state: FSMContext, redis: Redis
):
    """
    Обрабатывает выбор пака и запускает сессию обучения.

    - Формирует персональную очередь глаголов через _initialize_user_queue.
    - Извлекает первый глагол из очереди.
    - Сохраняет текущий глагол в FSM State (для отображения ответа, т.к. в очереди его уже нет).
    - Переключает состояние в ivc_thinking и показывает лицевую сторону карточки.
    """
    await callback.answer()
    await state.set_state(LearningStates.ivc_thinking)

    pack_service = PackService(redis_client=redis)
    await _initialize_user_queue(callback, pack_service)

    verb = await pack_service.get_verb(callback.from_user.id)
    await state.update_data(current_verb=verb)

    return await _show_ivc_original(callback, verb)


@router.callback_query(
    F.data == LearningKbCallbacks.NEXT_VERB,
    LearningStates.ivc_showing_answer,
)
async def cb_load_next_verb(callback: CallbackQuery, state: FSMContext, redis: Redis):
    """
    Обрабатывает переход к следующему глаголу после просмотра ответа.

    - Извлекает новую карточку из Redis-очереди пользователя.
    - Если очередь пуста: сбрасывает состояние и возвращает в меню выбора паков.
    - Если карточка есть: обновляет данные в State и показывает лицевую сторону.
    """
    await callback.answer()
    await state.set_state(LearningStates.ivc_thinking)
    pack_service = PackService(redis_client=redis)

    verb = await pack_service.get_verb(callback.from_user.id)
    if not verb:
        await state.set_state(LearningStates.select_pack)
        packs = await pack_service.get_packs()
        return await callback.message.edit_text(
            text=Texts.CHANGE_PACK, reply_markup=build_pack_selection_kb(packs)
        )

    await state.update_data(current_verb=verb)
    return await _show_ivc_original(callback, verb)


@router.callback_query(
    F.data == CardActionCallbacks.SHOW_ANSWER,
    LearningStates.ivc_thinking,
)
async def cb_show_ivc_answer(callback: CallbackQuery, state: FSMContext):
    """
    Отображает обратную сторону карточки (все формы глагола и примеры).

    - Получает сохраненный объект глагола из FSM State.
    - Переключает состояние в ivc_showing_answer.
    - Показывает V1-V3, переводы и примеры.
    """
    await callback.answer()
    await state.set_state(LearningStates.ivc_showing_answer)

    state_data = await state.get_data()
    verb = state_data.get("current_verb")
    return await _show_ivc_answer(callback, verb)


async def _show_ivc_original(callback: CallbackQuery, verb: dict):
    """Отображает лицевую сторону карточки неправильного глагола."""
    v1 = verb.get("v_1")
    ex_v1 = verb.get("v_1_example")

    text = f"🇬🇧 <b>{v1}</b>"
    if ex_v1:
        text += f"\n\n<i>Example:</i> {ex_v1}"

    await callback.message.edit_text(
        text=text,
        reply_markup=get_show_answer_kb(),
    )


async def _show_ivc_answer(callback: CallbackQuery, verb: dict):
    """
    Отображает цепочку форм (V1-V2-V3), общий перевод и три блока
    с примерами использования для каждой формы с их переводами.
    """
    v1 = verb.get("v_1", "")
    v2 = verb.get("v_2", "")
    v3 = verb.get("v_3", "")
    translation = verb.get("translation", "")

    ex1 = verb.get("v_1_example")
    tr1 = verb.get("v_1_example_translation")
    ex2 = verb.get("v_2_example")
    tr2 = verb.get("v_2_example_translation")
    ex3 = verb.get("v_3_example")
    tr3 = verb.get("v_3_example_translation")

    text = f"⚡️ <b>{v1} — {v2} — {v3}</b>\n" f"🇷🇺 {translation}"

    if ex1 or tr1:
        text += "\n\n🔹 <b>Infinitive:</b>\n"
        if ex1:
            text += f"<i>{ex1}</i>\n"
        if tr1:
            text += f"({tr1})"

    if ex2 or tr2:
        text += "\n\n🔸 <b>Past Simple:</b>\n"
        if ex2:
            text += f"<i>{ex2}</i>\n"
        if tr2:
            text += f"({tr2})"

    if ex3 or tr3:
        text += "\n\n🔹 <b>Participle II:</b>\n"
        if ex3:
            text += f"<i>{ex3}</i>\n"
        if tr3:
            text += f"({tr3})"

    await callback.message.edit_text(
        text=text,
        reply_markup=get_next_ivc_kb(),
    )


async def _initialize_user_queue(callback: CallbackQuery, pack_service: PackService):
    """
    Определяет режим заполнения очереди:
    - RANDOM_IVC: Собирает ID всех доступных паков.
    - Конкретный пак: Парсит ID из callback_data (формат 'pack_{id}').

    Передает полученный список ID в сервис для создания смешанной очереди.
    """
    if callback.data == LearningKbCallbacks.RANDOM_IVC:
        all_packs = await pack_service.get_packs()
        await pack_service.initialize_user_queue(
            telegram_id=callback.from_user.id,
            pack_ids=[p["id"] for p in all_packs],
        )
    else:
        pack_id = [int(callback.data.split("_")[1])]
        await pack_service.initialize_user_queue(
            telegram_id=callback.from_user.id,
            pack_ids=pack_id,
        )