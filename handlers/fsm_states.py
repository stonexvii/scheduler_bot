from aiogram.fsm.state import State, StatesGroup


class AddEvent(StatesGroup):
    wait = State()
