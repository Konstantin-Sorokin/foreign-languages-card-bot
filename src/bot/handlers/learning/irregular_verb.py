from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from bot.keyboards.learning import (
    get_next_verb_kb,
    get_show_verb_answer_kb,
    get_verb_groups_kb,
)
from bot.resources import AppResources
from bot.schemas.irregular_verb import IrregularVerbRead
from bot.texts.messages import CHANGE_VERB_GROUP, VERBS_FINISHED
from bot.utils.callbacks import LearningCallbacks
from bot.utils.enums import VerbGroup
from bot.utils.formatters import render_verb_back, render_verb_front

router = Router(name=__name__)


@router.callback_query(F.data == LearningCallbacks.IRREGULAR_VERBS)
async def open_irregular_verbs_menu(
    callback: CallbackQuery,
) -> None:
    """Show the irregular verb group selection menu."""

    if not isinstance(callback.message, Message):
        return

    await callback.message.edit_text(
        text=CHANGE_VERB_GROUP,
        reply_markup=get_verb_groups_kb(),
    )

    await callback.answer()


@router.callback_query(F.data.startswith(f"{LearningCallbacks.VERB_GROUP}:"))
async def open_verb_group(
    callback: CallbackQuery,
    resources: AppResources,
    user_id: int,
):
    """Start studying a specific group of irregular verbs."""
    if callback.data is None:
        return

    _, group = callback.data.rsplit(":", 1)
    verb = await resources.learning_service.start_verbs(
        user_id=user_id, group=VerbGroup(group)
    )

    await show_verb_front(callback, verb)
    await callback.answer()


@router.callback_query(F.data == LearningCallbacks.RANDOM_VERBS)
async def open_random_verbs(
    callback: CallbackQuery,
    resources: AppResources,
    user_id: int,
):
    """Start studying with random verbs from all groups."""
    verb = await resources.learning_service.start_verbs(user_id=user_id)

    await show_verb_front(callback, verb)
    await callback.answer()


@router.callback_query(F.data == LearningCallbacks.NEXT_VERB)
async def next_verb(
    callback: CallbackQuery,
    resources: AppResources,
    user_id: int,
):
    """Show the next verb in the current study session."""
    verb = await resources.learning_service.get_next_verb(
        user_id=user_id,
    )

    if verb is None and isinstance(callback.message, Message):
        await callback.message.edit_text(
            text=VERBS_FINISHED,
            reply_markup=get_verb_groups_kb(),
        )

        await callback.answer()
        return

    await show_verb_front(callback, verb)
    await callback.answer()


@router.callback_query(F.data == LearningCallbacks.SHOW_VERB_ANSWER)
async def show_verb_answer(
    callback: CallbackQuery,
    resources: AppResources,
    user_id: int,
):
    """Reveal the full conjugation of the current verb."""
    verb = await resources.learning_service.get_current_verb(
        user_id=user_id,
    )

    await show_verb_back(callback, verb)
    await callback.answer()


async def show_verb_front(
    callback: CallbackQuery,
    verb: IrregularVerbRead | None,
) -> None:
    """Display the verb's infinitive and ask the user to recall the forms."""
    if verb is None or not isinstance(callback.message, Message):
        return

    await callback.message.edit_text(
        text=render_verb_front(verb=verb),
        reply_markup=get_show_verb_answer_kb(),
    )


async def show_verb_back(
    callback: CallbackQuery,
    verb: IrregularVerbRead | None,
) -> None:
    """Display the full conjugation with examples."""
    if verb is None or not isinstance(callback.message, Message):
        return

    await callback.message.edit_text(
        text=render_verb_back(verb=verb),
        reply_markup=get_next_verb_kb(),
    )
