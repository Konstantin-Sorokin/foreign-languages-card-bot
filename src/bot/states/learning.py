from aiogram.fsm.state import State, StatesGroup


class LearningStates(StatesGroup):
    """
    Состояния (FSM) для процесса обучения.

    Ветки состояний:
    - Translation Cards (свои карточки): choosing_mode → tc_thinking → tc_checking → tc_waiting_evaluation
    - Irregular Verb Cards (неправильные глаголы): choosing_mode → select_pack → ivc_thinking → ivc_showing_answer
    """

    choosing_mode = State()

    # --- Режим Translation Cards ---
    tc_thinking = State()
    tc_checking = State()
    tc_waiting_evaluation = State()

    # --- Режим Irregular Verb Cards ---
    select_pack = State()
    ivc_thinking = State()
    ivc_showing_answer = State()
