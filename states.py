from aiogram.fsm.state import StatesGroup, State


class CallBackOnStart(StatesGroup):
    name = State()
    game = State()
    platform = State()
    poll = State()
