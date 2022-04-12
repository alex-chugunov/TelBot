from links import bot
import telebot


def get_main_menu(message):
    main_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_bit_rate = telebot.types.KeyboardButton("Курс биткоина")
    button_news = telebot.types.KeyboardButton("Новости")
    main_menu.add(button_bit_rate, button_news)
    bot.send_message(message.chat.id, 'Выберите: ', reply_markup=main_menu)


def get_submenu(message):
    submenu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_bit_usd = telebot.types.KeyboardButton("Доллар")
    button_bit_rur = telebot.types.KeyboardButton("Рубль")
    button_back = telebot.types.KeyboardButton("Назад")
    submenu.add(button_bit_usd, button_bit_rur, button_back)
    bot.send_message(message.chat.id, 'Выберите валюту:', reply_markup=submenu)