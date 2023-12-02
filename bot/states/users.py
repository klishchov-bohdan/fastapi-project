from aiogram.dispatcher.filters.state import StatesGroup, State


class SignIn(StatesGroup):
    password = State()


class SignUp(StatesGroup):
    password = State()
    email = State()


class AdminMe(StatesGroup):
    message = State()
    confirmation = State()


class UpdateEmail(StatesGroup):
    email = State()
