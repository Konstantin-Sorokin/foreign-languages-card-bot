from aiogram.fsm.state import State, StatesGroup


class AddCardStates(StatesGroup):
    input_original = State()
    input_translation = State()
    input_example = State()
    input_example_translation = State()
    waiting_action = State()
