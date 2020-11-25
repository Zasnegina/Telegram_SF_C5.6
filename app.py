import telebot
from config import keys, TOKEN
from extensions import CurrencyConvertor, APIException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def welcome(message: telebot.types.Message):
    text = 'Чтобы начать работу введите следующие параметры через пробел: \n<исходная валюта> \n<конечная валюта> ' \
           '\n<сумма>. \n Чтобы увидеть список всех доступных валют введите команду /values '
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Неверное количество параметров')

        base, quote, amount = values
        total_base = CurrencyConvertor.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Невозможно обработать команду.\n{e}')
    else:
        text = f'{amount} {base} = {total_base} {quote}'
        bot.send_message(message.chat.id, text)


bot.polling()
