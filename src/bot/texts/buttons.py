from bot.utils.enums import VerbGroup


class StartButtons:
    LEARNING = "📚 Обучение"
    ADD = "➕ Добавить"


class LearningButtons:
    MY_CARDS = "📕 Карточки"
    SHOW_ANSWER = "👁️ Показать ответ"
    KNOW = "✅ Знаю"
    DONT_KNOW = "❌ Не знаю"

    IRREGULAR_VERBS = "📘 Глаголы"
    RANDOM_VERBS = "🎲 Случайные"
    NEXT_VERB = "➡️ Далее"


class AddButtons:
    CARD = "📕 Своя карточка"
    PACK = "📦 Готовый пак"


class CardButtons:
    SAVE_WITHOUT_EXAMPLE = "💾 Сохранить без примера"
    SAVE = "💾 Сохранить"
    ADD_EXAMPLE = "➕ Добавить пример"
    CANCEL = "❌ Отмена"


class PackButtons:
    BACK = "⬅️ Назад"
    ADD = "➕ Добавить"


VERB_GROUP_BUTTONS = {
    VerbGroup.UNCHANGED: "🔁 Неизм.",
    VerbGroup.TD: "🔧 T-D",
    VerbGroup.VOWEL: "🔊 Гласные",
    VerbGroup.STRONG: "💪 Сложные",
}
