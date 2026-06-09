from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.keyboards.add_card_kbs import build_confirm_keyboard
from bot.states import AddCardStates
from bot.utils.constants import StartKbTexts, Texts

router = Router()


@router.message(F.text == StartKbTexts.ADD_CARD)
async def msg_add_new_card(
    message: Message,
    state: FSMContext,
):
    """
    Обработчик нажатия на кнопку добавления карточки.
    Устанавливает состояние ожидания ввода оригинала карты
    """

    await message.answer(
        Texts.INPUT_ORIGINAL_MSG,
    )
    await state.set_state(AddCardStates.input_original)


@router.message(AddCardStates.input_original, F.text)
async def msg_process_original(
    message: Message,
    state: FSMContext,
):
    """
    Обработчик ввода оригинала карточки. Проверяет ввод и вносит его во временное хранилище в state.
    Переводит состояние в ожидание ввода перевода карточки
    """
    original = message.text.strip()

    if not original:
        await message.answer("❌ Ввод не может быть пустым. Попробуйте еще раз.")
        return

    await state.update_data(original=original)
    await message.answer(Texts.INPUT_TRANSLATION_MSG)
    await state.set_state(AddCardStates.input_translation)


@router.message(AddCardStates.input_translation, F.text)
async def msg_process_translation(
    message: Message,
    state: FSMContext,
):
    """
    Обработчик ввода перевода карточки. Проверяет ввод и вносит его во временное хранилище в state.
    Показывает всю информацию о карточке и предлагает выбор - сохранить карточку, добавить примеры или отменить.
    """
    translation = message.text.strip()

    if not translation:
        await message.answer("❌ Перевод не может быть пустым.")
        return

    await state.update_data(translation=translation)
    data = await state.get_data()

    text = (
        f"📝 <b>Проверьте данные:</b>\n\n"
        f"🇬🇧 Слово/Словосочетание: <b>{data['original']}</b>\n"
        f"🇷🇺 Перевод: <b>{translation}</b>\n\n"
        f"Всё верно?"
    )

    await message.answer(
        text=text,
        reply_markup=build_confirm_keyboard(),
    )


@router.message(AddCardStates.input_example, F.text)
async def msg_process_example(
    message: Message,
    state: FSMContext,
):
    """
    Обработчик ввода примера на оригинальном языке.
    Проверяет ввод и вносит его во временное хранилище в state.
    Переводит состояние в ожидание ввода перевода данного примера
    """
    example = message.text.strip()

    if not example:
        await message.answer("❌ Ввод не может быть пустым. Попробуйте еще раз.")
        return

    await state.update_data(example=example)
    await message.answer(Texts.INPUT_TRANSLATION_MSG)
    await state.set_state(AddCardStates.input_example_translation)


@router.message(AddCardStates.input_example_translation, F.text)
async def msg_process_example_translation(
    message: Message,
    state: FSMContext,
):
    """
    Обработчик ввода перевода примера.
    Проверяет ввод и вносит его во временное хранилище в state.
    Показывает всю информацию о карточке и предлагает выбор - сохранить карточку или отменить.
    """
    example_translation = message.text.strip()

    if not example_translation:
        await message.answer("❌ Ввод не может быть пустым. Попробуйте еще раз.")
        return

    await state.update_data(example_translation=example_translation)
    data = await state.get_data()

    text = (
        f"📝 <b>Проверьте данные:</b>\n\n"
        f"🇬🇧 Слово/Словосочетание: <b>{data['original']}</b>\n"
        f"🇷🇺 Перевод: <b>{data['translation']}</b>\n\n"
        f"🇷🇺 Пример: <b>{data['example']}</b>\n"
        f"🇷🇺 Перевод примера: <b>{example_translation}</b>\n\n\n"
        f"Всё верно?"
    )

    await message.answer(
        text=text,
        reply_markup=build_confirm_keyboard(added_example=True),
    )
    # await state.update_data(example_translation=example_translation)
    # await message.answer(Texts.INPUT_TRANSLATION_MSG)
    # await state.set_state(AddCardStates.input_example_translation)
