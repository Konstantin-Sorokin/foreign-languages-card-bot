from aiogram.filters.callback_data import CallbackData

from bot.utils.enums import PackAction


class LearningCallbacks:
    TRANSLATION_CARDS = "learn:translation"
    SHOW_CARD_ANSWER = "learn:card_answer"
    KNOW = "learn:know"
    DONT_KNOW = "learn:dont_know"

    IRREGULAR_VERBS = "learn:verbs"
    VERB_GROUP = "learn:verb"
    RANDOM_VERBS = "learn:random"
    SHOW_VERB_ANSWER = "learn:verb_answer"
    NEXT_VERB = "learn:next_verb"


class AddCallbacks:
    CARD = "add:card"
    PACK = "add:pack"


class CardCallbacks:
    SAVE_WITHOUT_EXAMPLE = "card:save_wo_example"
    SAVE = "card:save"
    CANCEL = "card:cancel"
    ADD_EXAMPLE = "card:example"


class PackCallback(CallbackData, prefix="pack"):
    action: PackAction
    pack_id: int | None = None
    added: bool | None = None
