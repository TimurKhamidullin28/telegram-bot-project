from loader import bot
import handlers  # noqa
from utils.set_bot_commands import set_default_commands
from utils.create_all_models import create_models
from telebot import custom_filters

if __name__ == "__main__":
    create_models()
    set_default_commands(bot)
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.infinity_polling()
