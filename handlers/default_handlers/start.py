from telebot.types import Message
from loader import bot
from database.common.models import db, User
from peewee import IntegrityError
from keyboards.reply.main import menu_markup


@bot.message_handler(commands=["start"])
def bot_start(message: Message) -> None:
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    try:
        with db:
            User.create(
                user_id=user_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
            )
            bot.reply_to(message, f'Добро пожаловать в бот, который поможет найти любой фильм на сервисе "Кинопоиск"!')
    except IntegrityError:
        bot.reply_to(message, f"Рад вас снова видеть, {message.from_user.full_name}!")

    bot.send_message(message.from_user.id, 'Команды бота', reply_markup=menu_markup())
