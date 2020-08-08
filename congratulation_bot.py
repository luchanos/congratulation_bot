import telebot
import time
from requests import ReadTimeout
from pic_overlaper import congratulation_func
from envparse import env

TOKEN = env.str('TOKEN')
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['text'])
def quote_message_handler(message):
    image_to_send = congratulation_func(message.text)
    bot.send_photo(chat_id=message.chat.id, photo=image_to_send)


def telegram_polling():
    try:
        bot.polling(none_stop=True)
    except ReadTimeout as err:
        bot.stop_polling()
        time.sleep(3)
        telegram_polling()


if __name__ == '__main__':
    telegram_polling()
