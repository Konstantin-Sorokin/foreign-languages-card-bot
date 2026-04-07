from aiogram.fsm.state import State, StatesGroup


class AddCardStates(StatesGroup):
    input_original = State()
    input_translate = State()
    confirm = State()
