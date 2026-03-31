from aiogram.fsm.state import State, StatesGroup


class LearningStates(StatesGroup):
    selecting_type = State()
    showing_translate_card = State()
    showing_irregular_verb_card = State()
    showing_answer = State()
    evaluating = State()
