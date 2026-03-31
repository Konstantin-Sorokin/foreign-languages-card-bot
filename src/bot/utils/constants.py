START_COMMAND = "start"
HELP_COMMAND = "help"


class Texts:
    NEXT_VERB = "Следующий глагол"
    NEXT_CARD = "Следующая карточка"


class StartKbTexts:
    LEARNING = "📚 Обучение"
    ADD_CARD = "🎯 Новая карточка"


class LearningKbTexts:
    TRANSLATION_CARDS = "📕 Карточки"
    IRREGULAR_VERB_CARDS = "📘 Глаголы"


class LearningKbCallbacks:
    TRANSLATION_CARDS = "learn:translation"
    IRREGULAR_VERB_CARDS = "learn:verbs"


class CardActionTexts:
    SHOW_ANSWER = "👁️ Показать ответ"
    KNOW = "✅ Знаю"
    DONT_KNOW = "❌ Не знаю"
    KNOW_MESSAGE = "✅ Отлично! Идём дальше."
    DONT_KNOW_MESSAGE = "📝 Ничего страшного, повторим позже."


class CardActionCallbacks:
    SHOW_ANSWER = "card:show_answer"
    KNOW = "card:know"
    DONT_KNOW = "card:dont_know"


class AddCardTexts:
    INSTRUCTION = (
        "Введите слово/словосочетание\nв формате:\n\nx<b>Оригинал</b> - <b>Перевод</b>"
    )
    CONFIRM_TITLE = "Проверьте данные:"
    SUCCESS_MESSAGE = "📚 Добавлено в словарь!"
    CONFIRM = "💾 Сохранить"
    CANCEL = "❌ Отмена"


class AddCardCallbacks:
    CONFIRM = "add:save"
    CANCEL = "add:cancel"
