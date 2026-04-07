from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.keyboards.add_card_kbs import build_confirm_keyboard
from bot.states import AddCardStates
from bot.utils.constants import AddCardTexts, StartKbTexts

router = Router()


@router.message(F.text == StartKbTexts.ADD_CARD)
async def input_original_handler(
    message: Message,
    state: FSMContext,
):
    await message.answer(
        AddCardTexts.ADD_ORIGINAL_MESSAGE,
    )
    await state.set_state(AddCardStates.input_original)


@router.message(AddCardStates.input_original, F.text)
async def input_translate_handler(
    message: Message,
    state: FSMContext,
):
    if message.text is None:
        await message.answer("❌ Пожалуйста, отправьте текст")
        return

    if not message.text:
        await message.answer("Ввод не может быть пустым")
        return

    original = message.text.strip()
    await state.update_data(original=original)
    await message.answer(
        AddCardTexts.ADD_TRANSLATE_MESSAGE,
    )
    await state.set_state(AddCardStates.input_translate)


@router.message(AddCardStates.input_translate)
async def confirm_handler(
    message: Message,
    state: FSMContext,
):
    if message.text is None:
        await message.answer("❌ Пожалуйста, отправьте текст")
        return

    if not message.text:
        await message.answer("Ввод не может быть пустым")
        return

    data = await state.get_data()
    original = data.get("original")

    translation = message.text.strip()
    await state.update_data(translation=translation)

    await message.answer(
        f"{AddCardTexts.CONFIRM_MESSAGE}\n\n{original}\n{translation}",
        reply_markup=build_confirm_keyboard(),
    )
    await state.set_state(AddCardStates.confirm)
