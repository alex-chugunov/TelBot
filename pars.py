# https://github.com/Ynxela/rbc_parser
from bs4 import BeautifulSoup
from links import rbk
import requests
import json

URL = rbk


def get_soup(url):
    r = requests.get(url).text
    return BeautifulSoup(r, 'lxml')


def save_json(data):
    with open('rbk_data.json', "w") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def collect():
    news_data = {}

    soup = get_soup(URL)

    # Получаем все ссылки на новости
    news_links = soup.find('div', class_='main').find_all('a', {'class': ['main__big__link', 'main__feed__link']})

    link = news_links[1].get('href').split('?')[0]
    name = link
    news_data[name] = {}
    soup = get_soup(link)

    # Переходим на страницу для дальнейшенго парсинга
    article = soup.find('div', class_='article')
    category = article.find('a', class_='article__header__category')
    date = article.find('span', class_='article__header__date').get('content').replace('T', ' ').split('+')[0]
    title = article.find('span', class_='js-slide-title')
    image = article.find('div', class_='article__main-image')
    article_paragraphs = article.find_all('p')
    article_text = ''
    for paragraph in article_paragraphs:
        article_text += paragraph.text

    # Заполняем полученными данными news_data
    news_data[name]['link'] = link
    news_data[name]['date'] = date
    news_data[name]['text'] = article_text.replace('\xa0', '').replace('\n', '').replace('\r', '')

    try:
        news_data[name]['title'] = title.text
    except AttributeError:
        news_data[name]['title'] = 'Без заголовка'
    try:
        news_data[name]['category'] = category.text.replace('\n', '')
    except AttributeError:
        news_data[name]['category'] = 'Без категории'
    try:
        news_data[name]['image'] = image.find('img').get('src')
    except AttributeError:
        news_data[name]['image'] = 'Без обложки'

    save_json(news_data)
    text = news_data[name]['text']
    text = text[:300]
    text = text.rpartition('.')[0]+"." + f"\n{news_data[name]['link']}"
    return text
