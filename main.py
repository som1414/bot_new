import telebot
from config import currencies, TOKEN
from extensions import APIException, CurrencyConverter
import markups as m

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    text = 'Здравствуйте!\nЧтобы увидеть список доступных валют введите: /values\n\
Чтобы конвертировать валюту введите: /convert'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in currencies.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(commands=['convert'])
def convert(message: telebot.types.Message):
    text = 'Введите валюту из которой конвертировать: '
    bot.send_message(message.chat.id, text, reply_markup=m.currency_markup)
    bot.register_next_step_handler(message, original_handler)


def original_handler(message: telebot.types.Message):
    original = message.text.strip()
    text = 'Введите валюту в которую конвертировать: '
    bot.send_message(message.chat.id, text, reply_markup=m.currency_markup)
    bot.register_next_step_handler(message, result_handler, original)


def result_handler(message: telebot.types.Message, original):
    result = message.text.strip()
    text = 'Введите колличество конвертируемой валюты: '
    bot.send_message(message.chat.id, text, reply_markup=m.remove_markup)
    bot.register_next_step_handler(message, quantity_handler, original, result)


def quantity_handler(message: telebot.types.Message, original, result):
    quantity = message.text.strip()
    try:
        values = original, result, quantity
        answer = CurrencyConverter.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f'Ошибка в запросе\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Неизвестная ошибка\n{e}')
    else:
        bot.send_message(message.chat.id, answer)

if __name__ == '__main__':
    bot.infinity_polling()

