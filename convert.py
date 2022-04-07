import speech_recognition as sr
from configs import bot, token
import urllib.request
import subprocess
import requests
import json
import os

s = requests.session()


def wav2text(dest_filename, msg, file_name):
    r = sr.Recognizer()
    message = sr.AudioFile(dest_filename)

    with message as source:
        audio = r.record(source)
    try:
        result = r.recognize_google(audio, language="ru_RU")
        return format(result)
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


