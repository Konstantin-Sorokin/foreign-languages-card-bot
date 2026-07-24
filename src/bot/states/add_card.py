from aiogram.fsm.state import State, StatesGroup


class AddCardStates(StatesGroup):
    word = State()
    translation = State()
    example = State()
    example_translation = State()
