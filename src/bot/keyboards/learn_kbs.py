from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.constants import (
    CardActionCallbacks,
    CardActionTexts,
    LearningKbCallbacks,
    LearningKbTexts,
    Texts,
)


def get_learning_choice_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=LearningKbTexts.TRANSLATION_CARDS,
        callback_data=LearningKbCallbacks.TRANSLATION_CARDS,
    )
    builder.button(
        text=LearningKbTexts.IRREGULAR_VERB_CARDS,
        callback_data=LearningKbCallbacks.IRREGULAR_VERB_CARDS,
    )

    builder.adjust(2)
    return builder.as_markup()


def get_show_answer_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=CardActionTexts.SHOW_ANSWER, callback_data=CardActionCallbacks.SHOW_ANSWER
    )
    return builder.as_markup()


def get_evaluation_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text=CardActionTexts.KNOW, callback_data=CardActionCallbacks.KNOW)
    builder.button(
        text=CardActionTexts.DONT_KNOW, callback_data=CardActionCallbacks.DONT_KNOW
    )
    builder.adjust(2)
    return builder.as_markup()


def get_next_tc_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=Texts.NEXT_CARD,
        callback_data=LearningKbCallbacks.TRANSLATION_CARDS,
    )
    return builder.as_markup()


def get_next_ivc_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=Texts.NEXT_VERB,
        callback_data=LearningKbCallbacks.IRREGULAR_VERB_CARDS,
    )
    return builder.as_markup()
