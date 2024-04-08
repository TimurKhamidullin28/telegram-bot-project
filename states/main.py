from telebot.handler_backends import State, StatesGroup


class UserState(StatesGroup):
    film_title = State()
