from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    types = State()
    name = State()
    age = State()
    sex = State()
    country = State()
    city = State()
    about = State()
    photo = State()