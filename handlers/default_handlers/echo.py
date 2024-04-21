from telebot.types import Message

from loader import bot


@bot.message_handler(state=None)
def bot_echo(message: Message) -> None:
    """
    Функция-обработчик, в которую поступают сообщения без указанного состояния
    """
    bot.reply_to(
        message, f"Сообщение: {message.text}\nЧтобы бот работал, нужно отправить команду!"
    )
