from aiogram.fsm.state import StatesGroup, State


class CallBackOnStart(StatesGroup):
    user_id = State()
    name = State()
    game = State()
    platform = State()
    poll = State()
    reviewed = State()
    gamer_id = State()
    order_message_id = State()
