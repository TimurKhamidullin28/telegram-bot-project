from telebot.handler_backends import State, StatesGroup


class UserState(StatesGroup):
    """
    Класс, описывающий состояния, в которых может оказаться пользователь внутри сценария
    """
    film_title = State()
    genre_name = State()
    film_rating = State()
    quantity_films = State()
