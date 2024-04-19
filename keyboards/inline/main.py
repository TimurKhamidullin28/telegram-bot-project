from typing import List
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.common.models import Movie


def movies_markup(movies_lst: List[Movie]):
    movies = movies_lst
    markup = InlineKeyboardMarkup()
    for movie in movies:
        markup.add(InlineKeyboardButton(
            text=f'{str(*movie.name)} ({int(*movie.year)})',
            callback_data=int(*movie.id_movie))
                   )

    return markup


def genres_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Список жанров", callback_data="genres"))
    return markup
