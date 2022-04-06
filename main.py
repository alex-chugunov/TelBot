import requests
from datetime import datetime
import telebot
import sqlite3
import speech_recognition as sr
from telebot import types
import soundfile as sf
import urllib.request
import subprocess
import requests
import telebot
import json
import os


token = "5150010456:AAHnbuVK-HgkheMIoKtr19QZaS9SiU_-BCY"
bot = telebot.TeleBot(token)
s = requests.session()


def get_data(message):
    req = requests.get("https://yobit.net/api/3/ticker/btc_usd")
    response = req.json()
    sell_price = response["btc_usd"]["sell"]
    bot.send_message(
        message.chat.id,
        f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\nЦена битка в $: {sell_price}"
    )


def wav2text(dest_filename, msg, file_name):
    r = sr.Recognizer()
    message = sr.AudioFile(dest_filename)

    with message as source:
        audio = r.record(source)
    try:
        result = r.recognize_google(audio, language="ru_RU")
        return format(result)
        #bot.send_message(msg, format(result))
        os.remove(dest_filename)
        os.remove(file_name)

    except sr.UnknownValueError as ex:
        bot.send_message(msg, 'Не удалось распознать сообщение!\nГовори чётче 😕😡' + str(ex))
        os.remove(dest_filename)
        os.remove(file_name)


def audio2wav(file_id, msg):
    r = s.get('https://api.telegram.org/bot' + token + '/getFile?file_id=' + file_id)
    r = json.loads(r.text)

    file_path = r['result']['file_path']
    file_id = r['result']['file_id']

    url = 'https://api.telegram.org/file/bot' + token + '/' + file_path
    urllib.request.urlretrieve(url, file_id + '.oga')
    file_name = file_id + '.oga'

    src_filename = file_name
    dest_filename = file_name + '.wav'
    process = subprocess.run(['ffmpeg', '-i', src_filename, dest_filename])
    res = wav2text(dest_filename, msg, file_name)
    return res


def telegram_bot(token):
    @bot.message_handler(content_types=["voice"])
    def translate(message):
        word = audio2wav(message.voice.file_id, message.chat.id)
        examples = {"цена", "курс", "стоимость"}
        if word.lower() in examples:
            get_data(message)
        else:
            bot.send_message(message.chat.id, 'Нет такой команды!\nИли не удалось её распознать 😕' )

    @bot.message_handler(commands=["start"])
    def start_message(message):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        item = telebot.types.KeyboardButton("Цена $")
        markup.add(item)
        bot.send_message(message.chat.id,
                         'Привет, {0.first_name} \nБот работает 🤖 \nРад тебя видеть 😄'.format(message.from_user),
                         reply_markup=markup)
        bot.send_message(message.chat.id, "Чтобы получить стоимость биткоина в $, нажми на кнопку <Цена $>")
        bot.send_message(message.chat.id, 'Или можешь отправить голосовое сообщение\nПо типу: "цена", "курс", "стоимость"')

        connect = sqlite3.connect('users.db')
        connect.commit()
        cursor = connect.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS logins(
                        id INTEGER,
                        name TEXT
                )""")
        connect.commit()

        people_id = message.chat.id
        cursor.execute(f"SELECT id FROM logins WHERE id = {people_id}")
        data = cursor.fetchone()
        if data is None:
            # user_id = message.chat.id
            # us = str(message.from_user.username)
            # print(type(user_id))
            sql = "insert into logins values (?, ?)"
            cursor.execute(sql, (message.chat.id, message.from_user.first_name))
            connect.commit()

    @bot.message_handler(content_types=["text"])
    def send_text(message):
        if message.text.lower() == "price" or message.text == "Цена $":
            try:
                get_data(message)
            except Exception as ex:
                print(ex)
                bot.send_message(
                    message.chat.id,
                    "Ошибка"
                )
        else:
            bot.send_message(message.chat.id, "Неверная команда")

    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    telegram_bot(token)
