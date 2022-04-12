import unittest
from convert import audio2wav
from gets import test_get_data
from pars import collect

file_id = 'AwACAgIAAxkBAAIEimJVRxRswV4_ihP-2o_tOmmT1dDKAALvFAACwtmpSsul1wckvTCxIwQ'
msg = 229133725
# Питон не воспринимает объект message, пришлось отдельно тестить получение курса
message = {'content_type': 'text', 'message_id': 1177,
           'from_user': {'id': 229133725, 'first_name': 'Alexey', 'username': None, 'last_name': None},
           'date': 1649756649,
           'chat': {'type': 'private', 'last_name': None, 'first_name': 'Alexey', 'username': None, 'id': 229133725,
                    'title': None, 'all_members_are_administrators': None}, 'forward_from_chat': None,
           'forward_from': None, 'forward_date': None, 'reply_to_message': None, 'edit_date': None, 'text': 'Доллар',
           'entities': None, 'audio': None, 'document': None, 'photo': None, 'sticker': None, 'video': None,
           'voice': None, 'caption': None, 'contact': None, 'location': None, 'venue': None, 'new_chat_member': None,
           'left_chat_member': None, 'new_chat_title': None, 'new_chat_photo': None, 'delete_chat_photo': None,
           'group_chat_created': None, 'supergroup_chat_created': None, 'channel_chat_created': None,
           'migrate_to_chat_id': None, 'migrate_from_chat_id': None, 'pinned_message': None}
text = "Минздрав не исключает риска новой волны коронавируса в России, заявил глава ведомства Михаил Мурашко в интервью Наиле Аскер-заде на канале «Россия 24». «Мы видим, что в ряде стран сегодня уже подъем заболеваемости констатируют медицинские работники»,— сказал он.\nhttps://www.rbc.ru/society/12/04/2022/625534079a79472ad719d480"


class TestMyBot(unittest.TestCase):

    def test_work_audio(self):
        self.assertEqual(audio2wav(file_id, msg), 'новости')  # тестим распознавание

    # def test_work_usd(self):
    # self.assertEqual(test_get_data("btc_usd"), 42391.83242628)  # тестим курс, но до конца не можем, ибо курс
    # меняется ежесекундно

    def test_work_news(self):
        self.assertEqual(collect(), text)  # тестим получение новостей
