from typing import List
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.common.models import Movie


def movies_markup(movies_lst: List[Movie]) -> InlineKeyboardMarkup:
    """
    Функция, реализующая перечень кнопок на основе полученного на вход списка объектов класса Movie
    """
    movies = movies_lst
    markup = InlineKeyboardMarkup()
    for movie in movies:
        markup.add(InlineKeyboardButton(
            text=f'{str(*movie.name)} ({int(*movie.year)})',
            callback_data=int(*movie.id_movie))
                   )

    return markup


def genres_markup() -> InlineKeyboardMarkup:
    """
    Функция, реализующая кнопку-подсказку для пользователя.
    При нажатии на нее будет отображен перечень всех жанров
    """
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Список жанров", callback_data="genres"))
    return markup
