import telebot
from cofig import TOKEN, keys
from excentions import APIException, ConverterCurrency

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите комманду боту в следующем формате:\n<имя валюты> \
    <в какую валюту перевести> \
    <количество переводимой валюты>\nУвидеть список доступнык к конверсии валют: /values '
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

        if len(values) != 3: raise APIException('Количество параметров не совпадает')
        base, quote, amount = values

        total_base = ConverterCurrency.get_price(base, quote, amount)
        final_amount = float(amount) * float(total_base)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    else:
        text = f'Стоимость {amount} {base} в {quote} = {final_amount} {quote}'
        bot.send_message(message.chat.id, text)

bot.polling()
