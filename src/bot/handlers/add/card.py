from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.keyboards.add import get_add_card_confirm_kb
from bot.keyboards.start import get_start_kb
from bot.resources import AppResources
from bot.schemas.translation_card import TranslationCardCreate
from bot.states import AddCardStates
from bot.texts.messages import MAIN_MENU_HINT
from bot.utils.callbacks import AddCallbacks, CardCallbacks
from bot.utils.formatters import render_card_back

router = Router(name=__name__)


@router.callback_query(F.data == AddCallbacks.CARD)
async def start_add_card(
    callback: CallbackQuery,
    state: FSMContext,
):
    """Start the flow for adding a new translation card."""
    if not isinstance(callback.message, Message):
        return

    await state.set_state(AddCardStates.word)

    await callback.message.answer(
        "Введите оригинал:",
    )

    await callback.answer()


@router.message(AddCardStates.word)
async def process_word(
    message: Message,
    state: FSMContext,
):
    """Save the original word and ask for translation."""
    if not message.text:
        await message.answer("Отправь текст")
        return

    await state.update_data(
        original=message.text,
    )

    await state.set_state(AddCardStates.translation)

    await message.answer(
        "Введите перевод:",
    )


@router.message(AddCardStates.translation)
async def process_translation(
    message: Message,
    state: FSMContext,
):
    """Save the translation and show card preview."""
    if not message.text:
        await message.answer("Отправь текст")
        return

    await state.update_data(
        translation=message.text,
    )
    await state.set_state(None)

    data = await state.get_data()

    await message.answer(
        text=render_card_back(TranslationCardCreate.model_validate(data)),
        reply_markup=get_add_card_confirm_kb(has_example=False),
    )


@router.callback_query(F.data == CardCallbacks.ADD_EXAMPLE)
async def add_example(
    callback: CallbackQuery,
    state: FSMContext,
):
    """Start the flow for adding an example to the card."""
    await state.set_state(AddCardStates.example)

    await callback.message.answer(
        "Введите пример:",
    )

    await callback.answer()


@router.message(AddCardStates.example)
async def process_example(
    message: Message,
    state: FSMContext,
):
    """Save the example text and ask for its translation."""
    if not message.text:
        await message.answer("Отправь текстом 🙂")
        return

    await state.update_data(
        example=message.text,
    )

    await state.set_state(AddCardStates.example_translation)

    await message.answer(
        "Введите перевод примера:",
    )


@router.message(AddCardStates.example_translation)
async def process_example_translation(
    message: Message,
    state: FSMContext,
):
    """Save the example translation and show final card preview."""
    if not message.text:
        await message.answer("Отправь текстом 🙂")
        return

    await state.update_data(
        example_translation=message.text,
    )
    await state.set_state(None)
    data = await state.get_data()
    await message.answer(
        text=render_card_back(TranslationCardCreate.model_validate(data)),
        reply_markup=get_add_card_confirm_kb(has_example=True),
    )


@router.callback_query(F.data == CardCallbacks.SAVE)
@router.callback_query(F.data == CardCallbacks.SAVE_WITHOUT_EXAMPLE)
async def save_card(
    callback: CallbackQuery,
    state: FSMContext,
    resources: AppResources,
    user_id: int,
):
    """Persist the card and clear the FSM state."""
    if not isinstance(callback.message, Message):
        return
    data = await state.get_data()

    await resources.card_service.create(
        user_id=user_id,
        card_data=TranslationCardCreate.model_validate(data),
    )
    await state.clear()
    await callback.message.edit_text("✅ Карточка сохранена!")
    await callback.answer()


@router.callback_query(F.data == CardCallbacks.CANCEL)
async def cancel_add_card(
    callback: CallbackQuery,
    state: FSMContext,
):
    """Cancel card creation and return to main menu."""
    await state.clear()

    if not isinstance(callback.message, Message):
        return

    await callback.message.edit_text("❌ Добавление карточки отменено.")

    await callback.message.answer(
        text=MAIN_MENU_HINT,
        reply_markup=get_start_kb(),
    )

    await callback.answer()
