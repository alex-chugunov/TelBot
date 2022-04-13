import unittest
from convert import audio2wav
from gets import test_get_data
from pars import collect

file_id = 'AwACAgIAAxkBAAIEimJVRxRswV4_ihP-2o_tOmmT1dDKAALvFAACwtmpSsul1wckvTCxIwQ'
msg = 229133725
text = 'Падение биткоина сменилось консолидацией выше уровня $ 40000\nhttps://cryptonews.net/ru/news/bitcoin/4991037/'


class TestMyBot(unittest.TestCase):

    def test_work_audio(self):
        self.assertEqual(audio2wav(file_id, msg), 'новости')  # тестим распознавание

    # def test_work_usd(self):
    # self.assertEqual(test_get_data("btc_usd"), 42391.83242628)  # тестим курс, но до конца не можем, ибо курс
    # меняется ежесекундно

    def test_work_news(self):
        self.assertEqual(collect(), text)  # тестим получение новостей
