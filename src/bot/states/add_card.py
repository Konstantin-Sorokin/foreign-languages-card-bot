from aiogram.fsm.state import State, StatesGroup


class AddCardStates(StatesGroup):
    """
    Состояния (FSM) для процесса добавления новой карточки пользователем.

    Последовательность:
    input_original → input_translation → [input_example → input_example_translation] → waiting_action
    Блок с примером опционален.
    """

    input_original = State()
    input_translation = State()
    input_example = State()
    input_example_translation = State()
    waiting_action = State()
