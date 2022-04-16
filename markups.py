from telebot import types
from config import currencies

currency_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
remove_markup = reply_markup=types.ReplyKeyboardRemove()
buttons = []
for key in currencies.keys():
    buttons.append(types.KeyboardButton(key.capitalize()))
currency_markup.add(*buttons)
pass