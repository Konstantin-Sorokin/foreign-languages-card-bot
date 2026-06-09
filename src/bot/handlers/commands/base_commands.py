from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.keyboards.start_kb import get_start_kb
from bot.utils.constants import (
    HELP_COMMAND,
    START_COMMAND,
    LearningKbTexts,
    StartKbTexts,
)

router = Router(name=__name__)


@router.message(Command(START_COMMAND))
async def cmd_start(message: types.Message, state: FSMContext):
    """Главное меню бота."""
    await state.clear()

    start_text = (
        "👋 <b>Привет! Добро пожаловать в тренажер английского.</b>\n\n"
        "Что будем делать?\n\n"
        f"<b>{StartKbTexts.LEARNING}</b>\n"
        "Запустить режим повторения. Ты сможешь выбрать:\n"
        "• Свои добавленные карточки\n"
        "• Готовые паки с неправильными глаголами\n\n"
        f"<b>{StartKbTexts.ADD_CARD}</b>\n"
        "Добавить новое слово или фразу в свою личную базу.\n\n"
        "Выбери действие ниже 👇"
    )

    await message.answer(
        text=start_text,
        reply_markup=get_start_kb(),
    )


@router.message(Command(HELP_COMMAND))
async def cmd_help(message: types.Message):
    """Справочная информация по использованию бота."""

    help_text = (
        "👋 <b>Привет! Я твой персональный тренажер английского.</b>\n\n"
        "📚 <b>Режимы обучения:</b>\n\n"
        f"<b>{LearningKbTexts.TRANSLATION_CARDS}</b>\n"
        f"• Сначала добавь свои слова через кнопку <b>{StartKbTexts.ADD_CARD}</b>.\n"
        "• Учи только то, что добавил сам. Идеально для личных списков!\n\n"
        f"<b>{LearningKbTexts.IRREGULAR_VERB_CARDS}</b>\n"
        "• Готовая база с примерами и переводами.\n"
        "• Выбери тематический пак или учи всё вперемешку.\n"
        "• Запоминай все 3 формы глагола в контексте.\n\n"
        "⚙️ <b>Команды:</b>\n"
        "/start — Главное меню\n"
        "/help — Эта справка\n\n"
        "💡 <i>Начни с добавления первых 5-10 слов и запусти обучение!</i>"
    )

    await message.answer(help_text)
