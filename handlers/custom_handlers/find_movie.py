import json
from datetime import datetime
import api.main
from api.main import get_movie
from database.common.models import db, History, User
from keyboards.inline.main import movies_markup
from loader import bot
from states.main import UserState
from telebot.types import Message
from utils.create_movie_list import create_movie_list


@bot.message_handler(state="*", commands=["movie"])
def find_movie(message: Message) -> None:
    user_id = message.from_user.id
    if User.get_or_none(User.user_id == user_id) is None:
        bot.reply_to(message, "Вы не зарегистрированы. Напишите /start")
        return

    bot.send_message(user_id, "Введите название фильма")
    bot.set_state(message.from_user.id, UserState.film_title)
    with bot.retrieve_data(message.from_user.id) as data:
        data["user_history"] = {"user_id": user_id}


@bot.message_handler(content_types=['text'], state=UserState.film_title)
def process_film_title(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id) as data:
        data["user_history"]["title"] = message.text
        data["user_history"]["created_at"] = datetime.now()
    with db:
        History(**data["user_history"])
    response = api.main.find_movie(title=message.text)
    new_data = json.loads(response.text)
    lst_movies = create_movie_list(new_data['docs'])
    bot.send_message(message.from_user.id, 'Выберите фильм из списка:', reply_markup=movies_markup(lst_movies))

    bot.delete_state(message.from_user.id)


@bot.callback_query_handler(func=lambda message: True)
def callback_query(message):
    bot.send_message(message.from_user.id, *get_movie(message.data))
