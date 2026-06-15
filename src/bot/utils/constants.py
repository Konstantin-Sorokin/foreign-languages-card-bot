START_COMMAND = "start"
HELP_COMMAND = "help"


class Texts:
    SELECT_TYPE_LEARNING = "🎯 Выберите тип обучения:"
    CHANGE_PACK = "📦 Выберите пак с глаголами"
    NEXT_VERB = "⏭️ Следующий глагол"
    NEXT_CARD = "⏭️ Следующая карточка"
    KNOW = "✅ Отлично! Идём дальше."
    DONT_KNOW = "📝 Ничего страшного, повторим позже."
    NO_CARDS = "⚠️ Карточки для обучения отсутствуют, добавьте новые"

    INPUT_ORIGINAL_MSG = "✍️ Введите оригинал слова / словосочетания"
    INPUT_TRANSLATION_MSG = "✍️ Введите перевод слова / словосочетания"
    INPUT_EXAMPLE_MSG = "✍️ Введите оригинал примера"
    INPUT_EXAMPLE_TRANSLATION_MSG = "✍️ Введите перевод примера"
    CONFIRM_MSG = "📋 Проверьте данные:"
    SUCCESS_MSG = "📚 Добавлено в словарь!"
    CANCEL_MSG = "❌ Добавление отменено"


class StartKbTexts:
    LEARNING = "📚 Обучение"
    ADD_CARD = "🎯 Новая карточка"


class LearningKbTexts:
    TRANSLATION_CARDS = "📕 Карточки"
    IRREGULAR_VERB_CARDS = "📘 Глаголы"
    RANDOM_IVC = "📘 Случайные глаголы"


class LearningKbCallbacks:
    TRANSLATION_CARDS = "learn:translation"
    IRREGULAR_VERB_CARDS = "learn:verbs"
    NEXT_CARD = "learn:next"
    NEXT_VERB = "learn:next_ivc"
    RANDOM_IVC = "learn:random_ivc"


class CardActionTexts:
    SHOW_ANSWER = "👁️ Показать ответ"
    KNOW = "✅ Знаю"
    DONT_KNOW = "❌ Не знаю"


class CardActionCallbacks:
    SHOW_ANSWER = "card:show_answer"
    KNOW = "card:know"
    DONT_KNOW = "card:dont_know"


class AddCardTexts:
    CONFIRM_WO_EXAMPLE = "💾 Сохранить без примера"
    CONFIRM_W_EXAMPLE = "💾 Сохранить"
    CANCEL = "❌ Отмена"
    ADD_EXAMPLE = "➕ Добавить пример"


class AddCardCallbacks:
    CONFIRM_WO_EXAMPLE = "add:save_wo_example"
    CONFIRM_W_EXAMPLE = "add:save"
    CANCEL = "add:cancel"
    ADD_EXAMPLE = "add:example"