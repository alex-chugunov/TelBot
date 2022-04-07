from configs import bot, token
from datetime import datetime
from convert import audio2wav
from pars import collect
from teldb import record
import requests
import telebot


def get_data(message, monetary):
    req = requests.get("https://yobit.net/api/3/ticker/" + monetary)
    response = req.json()
    sell_price = response[monetary]["sell"]
    bot.send_message(message.chat.id, f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\nЦена биткоина: {sell_price}")


def get_news(message):
    last_rbk_post = collect()
    bot.send_message(message.chat.id, f"Статья с РБК:\n{last_rbk_post}")


def telegram_bot(token):
    @bot.message_handler(content_types=["voice"])
    def translate(message):
        word = audio2wav(message.voice.file_id, message.chat.id)
        examples_us = {"цена доллар", "курс в долларах", "доллар"}
        examples_ru = {"цена рубль", "курс в рублях", "рубль"}
        examples_news = {"новости", "последние новости"}
        if word.lower() in examples_us:
            words = "btc_usd"
        elif word.lower() in examples_ru:
            words = "btc_rur"
        elif word.lower() in examples_news:
            get_news(message)
        else:
            bot.send_message(message.chat.id, 'Нет такой команды!\nИли не удалось её распознать 😕')
        get_data(message, words)

    @bot.message_handler(commands=["start"])
    def start_message(message):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = telebot.types.KeyboardButton("Цена")
        item2 = telebot.types.KeyboardButton("Новости")
        markup.add(item1, item2)
        bot.send_message(message.chat.id, 'Привет, {0.first_name} \nБот работает 🤖 \nРад тебя видеть 😄'.format(message.from_user), reply_markup=markup)
        bot.send_message(message.chat.id, 'Чтобы получить стоимость биткоина, нажми на кнопку <Цена>, а затем '
                                          'интересующую тебя валюту\nИли можешь получить последнюю новость с РБК 😄')
        bot.send_message(message.chat.id, 'Также можешь отправить голосовое сообщение для получения курса биткоина или '
                                          'новостей\nПример:\nКурс в долларах — "цена доллар", "курс в долларах", '
                                          '"доллар"\nКурс в рублях — "цена рубль", "курс в рублях", "рубль"\nНовости '
                                          '— "новости", "последние новости" ')
        record(message)

    @bot.message_handler(content_types=["text"])
    def send_text(message):
        try:
            if message.text.lower() == "price" or message.text == "Цена":
                markup2 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
                item3 = telebot.types.KeyboardButton("Доллар")
                item4 = telebot.types.KeyboardButton("Рубль")
                back = telebot.types.KeyboardButton("Назад")
                markup2.add(item3, item4, back)
                bot.send_message(message.chat.id, 'Выберите валюту:', reply_markup=markup2)
            if message.text == "Доллар":
                get_data(message, "btc_usd")
            if message.text == "Рубль":
                get_data(message, "btc_rur")
            if message.text == "Назад":
                markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = telebot.types.KeyboardButton("Цена")
                item2 = telebot.types.KeyboardButton("Новости")
                markup.add(item1, item2)
                bot.send_message(message.chat.id, 'Выберите: ', reply_markup=markup)

            if message.text.lower() == "news" or message.text == "Новости":
                get_news(message)

        except Exception as ex:
            print(ex)
            bot.send_message(message.chat.id, "Ошибка")
    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    telegram_bot(token)
