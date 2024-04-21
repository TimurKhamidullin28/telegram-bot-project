from telebot.types import BotCommand
from config_data.config import DEFAULT_COMMANDS


def set_default_commands(bot):
    """
    Функция, которая задает основные команды,
    к которым пользователь может обратиться в Telegram-боте через кнопку 'Меню'
    """
    bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS]
    )
