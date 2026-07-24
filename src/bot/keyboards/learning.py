from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.texts.buttons import VERB_GROUP_BUTTONS, LearningButtons
from bot.utils.callbacks import LearningCallbacks


def get_learning_menu_kb() -> InlineKeyboardMarkup:
    """Keyboard for choosing the learning mode."""
    builder = InlineKeyboardBuilder()

    builder.button(
        text=LearningButtons.MY_CARDS,
        callback_data=LearningCallbacks.TRANSLATION_CARDS,
    )
    builder.button(
        text=LearningButtons.IRREGULAR_VERBS,
        callback_data=LearningCallbacks.IRREGULAR_VERBS,
    )

    builder.adjust(2)
    return builder.as_markup()


def get_verb_groups_kb() -> InlineKeyboardMarkup:
    """Keyboard for selecting an irregular verb group."""
    builder = InlineKeyboardBuilder()

    for group, text in VERB_GROUP_BUTTONS.items():
        builder.button(
            text=text, callback_data=f"{LearningCallbacks.VERB_GROUP}:{group.value}"
        )

    builder.button(
        text=LearningButtons.RANDOM_VERBS, callback_data=LearningCallbacks.RANDOM_VERBS
    )
    builder.adjust(2)

    return builder.as_markup()


def get_show_card_answer_kb() -> InlineKeyboardMarkup:
    """Button to reveal the card answer."""
    builder = InlineKeyboardBuilder()
    builder.button(
        text=LearningButtons.SHOW_ANSWER,
        callback_data=LearningCallbacks.SHOW_CARD_ANSWER,
    )
    return builder.as_markup()


def get_show_verb_answer_kb() -> InlineKeyboardMarkup:
    """Button to reveal the verb conjugation."""
    builder = InlineKeyboardBuilder()
    builder.button(
        text=LearningButtons.SHOW_ANSWER,
        callback_data=LearningCallbacks.SHOW_VERB_ANSWER,
    )
    return builder.as_markup()


def get_evaluation_kb() -> InlineKeyboardMarkup:
    """Keyboard for self-assessment: 'Know' / 'Don't know'."""
    builder = InlineKeyboardBuilder()

    builder.button(text=LearningButtons.KNOW, callback_data=LearningCallbacks.KNOW)
    builder.button(
        text=LearningButtons.DONT_KNOW, callback_data=LearningCallbacks.DONT_KNOW
    )
    builder.adjust(2)
    return builder.as_markup()


def get_next_verb_kb() -> InlineKeyboardMarkup:
    """Button to proceed to the next verb."""
    builder = InlineKeyboardBuilder()

    builder.button(
        text=LearningButtons.NEXT_VERB,
        callback_data=LearningCallbacks.NEXT_VERB,
    )

    return builder.as_markup()
