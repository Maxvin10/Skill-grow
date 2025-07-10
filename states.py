from aiogram.fsm.state import State, StatesGroup

class sign(StatesGroup):
    firstname = State()
    lastname = State()
    age = State()
    nomer = State()
