from links import bot, burse
from datetime import datetime
from pars import collect
import requests


def get_data(message, monetary, hint):
    req = requests.get(burse + monetary)
    response = req.json()
    sell_price = response[monetary]["sell"]
    bot.send_message(message.chat.id,
                     f"{datetime.now().strftime('%H:%M   %d-%m-%Y')}" + f"\nКурс биткоина: {float(sell_price):g}\n{hint}")


def get_usd(message, monetary="btc_usd", hint="в долларах"):
    get_data(message, monetary, hint)


def get_rur(message, monetary="btc_rur", hint="в рублях"):
    get_data(message, monetary, hint)


def get_news(message):
    last_rbk_post = collect()
    bot.send_message(message.chat.id, f"Статья с РБК:\n{last_rbk_post}")


def test_get_data(monetary):
    req = requests.get(burse + monetary)
    response = req.json()
    sell_price = response[monetary]["sell"]
    return sell_price