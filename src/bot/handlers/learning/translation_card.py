from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from bot.keyboards.learning import get_evaluation_kb, get_show_card_answer_kb
from bot.keyboards.start import get_start_kb
from bot.resources import AppResources
from bot.schemas.translation_card import TranslationCardRead
from bot.texts.messages import CARDS_FINISHED, MAIN_MENU_HINT, NO_CARDS
from bot.utils.callbacks import LearningCallbacks
from bot.utils.formatters import render_card_back, render_card_front

router = Router(name=__name__)


@router.callback_query(F.data == LearningCallbacks.TRANSLATION_CARDS)
async def start_translation_cards(
    callback: CallbackQuery,
    resources: AppResources,
    user_id: int,
) -> None:
    """Start reviewing due translation cards."""
    card = await resources.learning_service.get_next_card(user_id=user_id)

    if card is None:
        await show_no_cards(callback)
        await callback.answer()
        return

    await show_translation_card(
        callback=callback,
        card=card,
    )

    await callback.answer()


@router.callback_query(F.data == LearningCallbacks.SHOW_CARD_ANSWER)
async def show_card_answer(
    callback: CallbackQuery,
    resources: AppResources,
    user_id: int,
) -> None:
    """Reveal the translation and example for the current card."""
    card = await resources.learning_service.get_current_card(
        user_id=user_id,
    )

    await show_translation_card_back(callback, card)

    await callback.answer()


@router.callback_query(F.data == LearningCallbacks.KNOW)
async def answer_card_known(
    callback: CallbackQuery,
    resources: AppResources,
    user_id: int,
) -> None:
    """Mark the current card as known and proceed."""
    await handle_card_answer(
        callback=callback,
        resources=resources,
        user_id=user_id,
        success=True,
    )

    await callback.answer()


@router.callback_query(F.data == LearningCallbacks.DONT_KNOW)
async def answer_card_unknown(
    callback: CallbackQuery,
    resources: AppResources,
    user_id: int,
) -> None:
    """Mark the current card as unknown and schedule a re-check."""
    await handle_card_answer(
        callback=callback,
        resources=resources,
        user_id=user_id,
        success=False,
    )

    await callback.answer()


async def handle_card_answer(
    callback: CallbackQuery,
    resources: AppResources,
    user_id: int,
    success: bool,
) -> None:
    """Process the answer and show the next card if available."""
    card = await resources.learning_service.process_answer(
        user_id=user_id,
        success=success,
    )

    if card is None:
        await show_cards_finished(callback)
        return

    await show_translation_card(callback, card)


async def show_translation_card(
    callback: CallbackQuery,
    card: TranslationCardRead,
) -> None:
    """Display the card's original text and a button to reveal the answer."""
    if not isinstance(callback.message, Message):
        return

    await callback.message.edit_text(
        text=render_card_front(card), reply_markup=get_show_card_answer_kb()
    )


async def show_translation_card_back(
    callback: CallbackQuery,
    card: TranslationCardRead | None,
) -> None:
    """Display the card's translation and evaluation buttons."""
    if card is None or not isinstance(callback.message, Message):
        return

    await callback.message.edit_text(
        text=render_card_back(card),
        reply_markup=get_evaluation_kb(),
    )


async def show_cards_finished(callback: CallbackQuery) -> None:
    """Notify the user that all cards have been reviewed."""
    if not isinstance(callback.message, Message):
        return

    await callback.message.edit_text(text=CARDS_FINISHED)
    await callback.message.answer(text=MAIN_MENU_HINT, reply_markup=get_start_kb())


async def show_no_cards(callback: CallbackQuery) -> None:
    """Notify the user that no cards are available for review."""
    if not isinstance(callback.message, Message):
        return

    await callback.message.edit_text(text=NO_CARDS)
    await callback.message.answer(text=MAIN_MENU_HINT, reply_markup=get_start_kb())
