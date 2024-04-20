from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def menu_markup():
    keyboard_markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_1 = KeyboardButton('/movie')
    btn_2 = KeyboardButton('/genre_and_rt')
    btn_3 = KeyboardButton('/history')
    btn_4 = KeyboardButton('/help')
    keyboard_markup.add(btn_1, btn_2, btn_3, btn_4)

    return keyboard_markup
