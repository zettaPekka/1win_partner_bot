from aiogram.fsm.state import State, StatesGroup


class UserState(StatesGroup):
    gambling_id = State()