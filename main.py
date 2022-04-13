from dictelbt import get_main_menu, get_submenu
from gets import get_news, get_usd, get_rur
from links import bot, token
from convert import audio2wav
from teldb import record
import telebot


def telegram_bot(token):
    @bot.message_handler(content_types=["voice"])
    def translate(message):
        voice_in_word = audio2wav(message.voice.file_id, message.chat.id)
        dic_voices_usd = {"цена доллар", "курс в долларах", "доллар"}
        dic_voices_rur = {"цена рубль", "курс в рублях", "рубль"}
        dic_voices_news = {"новости", "последние новости", "биткоин"}
        if voice_in_word.lower() in dic_voices_usd:
            get_usd(message)
        elif voice_in_word.lower() in dic_voices_rur:
            get_rur(message)
        elif voice_in_word.lower() in dic_voices_news:
            get_news(message)
        else:
            bot.send_message(message.chat.id, 'Нет такой команды!\nИли не удалось её распознать 😕')

    @bot.message_handler(commands=["start"])
    def start_message(message):
        main_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_bit_rate = telebot.types.KeyboardButton("Курс биткоина")
        button_news = telebot.types.KeyboardButton("Новости")
        main_menu.add(button_bit_rate, button_news)
        bot.send_message(message.chat.id, 'Привет, {0.first_name} \nБот работает 🤖 \nРад тебя видеть 😄'.format(message.from_user), reply_markup=main_menu)
        bot.send_message(message.chat.id, 'Чтобы получить стоимость биткоина, нажми на кнопку <Курс биткоина>, а затем '
                                          'интересующую тебя валюту\nИли можешь получить последнюю новость, связанную с биткоином')
        bot.send_message(message.chat.id, 'Также можешь отправить голосовое сообщение для получения курса биткоина или '
                                          'новостей\nПример:\nКурс в долларах — "цена доллар", "курс в долларах", '
                                          '"доллар"\nКурс в рублях — "цена рубль", "курс в рублях", "рубль"\nНовости '
                                          '— "новости", "последние новости", "биткоин" ')
        record(message)

    @bot.message_handler(content_types=["text"])
    def send_text(message):
        try:
            operations = {
                "Курс биткоина": get_submenu,
                "Доллар": get_usd,
                "Рубль": get_rur,
                "Назад": get_main_menu,
                "Новости": get_news,
            }
            operations[message.text](message)
        except Exception as ex:
            print(ex)
            bot.send_message(message.chat.id, "Ошибка" + str(ex))
    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    telegram_bot(token)

