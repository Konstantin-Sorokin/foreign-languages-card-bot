from aiogram.fsm.state import State, StatesGroup


class LearningStates(StatesGroup):
    choosing_mode = State()

    # --- Режим Translation Cards ---
    tc_thinking = State()
    tc_checking = State()
    tc_waiting_evaluation = State()

    # --- Режим Irregular Verb Cards ---
    select_pack = State()
    ivc_thinking = State()
    ivc_showing_answer = State()
