from telebot.types import List, Message
from database.common.models import History
from database.functions import checkout_user, user_history_info
from loader import bot


@bot.message_handler(state="*", commands=["history"])
def handle_history(message: Message) -> None:
    user_id = message.from_user.id
    user = checkout_user(user_id)
    if user is None:
        bot.reply_to(message, "Вы не зарегистрированы. Напишите /start")
        return

    history_lst: List[History] = user_history_info(user)

    result = list()
    result.append("Ваша история поиска:\n")
    result.extend(map(str, history_lst))

    if not result:
        bot.send_message(message.from_user.id, "У вас ещё нет фильмов в истории поиска")
        return

    bot.send_message(message.from_user.id, "\n".join(result))
