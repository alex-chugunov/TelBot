from bs4 import BeautifulSoup
from links import url_pars
import requests
import random


def get_soup(url_pars):
    r = requests.get(url_pars).text
    return BeautifulSoup(r, 'lxml')


def collect():
    soup = get_soup(url_pars)
    news = []
    items = soup.find_all('div', class_='row news-item start-xs')
    for item in items:
        itemTitle = item.find('a', class_='title').text
        itemLink = item.find('a', href=True)
        itemLink = 'https://cryptonews.net' + itemLink['href']
        text = itemTitle + f"\n{itemLink}"
        news.append(text)
    random_news = random.choice(news)
    return random_news
