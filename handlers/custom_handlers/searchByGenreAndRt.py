from telebot.types import Message
from api.main import get_movie, find_by_genre_and_rt
from database.functions import checkout_user
from keyboards.inline.main import movies_markup
from loader import bot
from states.main import UserState
from utils.create_movie_list import create_movie_list


@bot.message_handler(state="*", commands=["genre_and_rt"])
def find_by_genre(message: Message) -> None:
    user_id = message.from_user.id
    if checkout_user(user_id) is None:
        bot.reply_to(message, "Вы не зарегистрированы. Напишите /start")
        return

    bot.send_message(user_id, "Введите интересующий Вас жанр")
    bot.set_state(message.from_user.id, UserState.genre_name)


@bot.message_handler(state=UserState.genre_name)
def process_genre_name(message: Message) -> None:
    if message.text.isalpha():
        bot.send_message(message.from_user.id, 'Теперь введите минимальный рейтинг, который должен быть у фильма')
        bot.set_state(message.from_user.id, UserState.film_rating)

        with bot.retrieve_data(message.from_user.id) as data:
            data["genre"] = message.text
    else:
        bot.send_message(message.from_user.id, 'Название жанра состоит только из букв')


@bot.message_handler(state=UserState.film_rating)
def process_film_rating(message: Message) -> None:
    try:
        if float(message.text):
            bot.send_message(message.from_user.id, 'Сколько фильмов вывести на экран?\nМаксимум 250')
            bot.set_state(message.from_user.id, UserState.quantity_films)

            with bot.retrieve_data(message.from_user.id) as data:
                data["rating"] = message.text
    except ValueError:
        bot.send_message(message.from_user.id, 'Рейтинг фильма может быть только числом')


@bot.message_handler(state=UserState.quantity_films)
def process_quantity_films(message: Message) -> None:
    if message.text.isdigit():
        with bot.retrieve_data(message.from_user.id) as data:
            data["total_films"] = message.text

        response = find_by_genre_and_rt(genre_name=data["genre"],
                                        rating=data["rating"],
                                        quantity=data["total_films"])
        lst_movies = create_movie_list(response['docs'])
        bot.send_message(message.from_user.id, 'Выберите фильм из списка:', reply_markup=movies_markup(lst_movies))
        bot.delete_state(message.from_user.id)
    else:
        bot.send_message(message.from_user.id, 'Введите число фильмов, пожалуйста')


@bot.callback_query_handler(func=lambda message: True)
def callback_query(message):
    bot.send_message(message.from_user.id, *get_movie(message.data))
