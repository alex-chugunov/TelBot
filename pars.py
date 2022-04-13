from bs4 import BeautifulSoup
from links import url_pars
import requests


def get_soup(url_pars):
    r = requests.get(url_pars).text
    return BeautifulSoup(r, 'lxml')


def collect():
    soup = get_soup(url_pars)
    items = soup.find('div', class_='row news-item start-xs')
    itemTitle = items.find('a', class_='title').text
    itemLink = items.find('a', href=True)
    itemLink = 'https://cryptonews.net' + itemLink['href']
    text = itemTitle + f"\n{itemLink}"
    return text
