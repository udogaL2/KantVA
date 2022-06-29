import requests
from bs4 import BeautifulSoup as BS
from random import choice
import qrcode

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.3.684 Yowser/2.5 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'ru,en;q=0.9,es;q=0.8'
}
session = requests.Session()

with open('quotes.txt', 'r') as f:
    quotes = f.read().strip().split('\n')
    f.close()


def get_quotes():
    return choice(quotes)


def generate_nearest_event():
    html = session.get('https://afisha.yandex.ru/kaliningrad/selections/nearest-events', headers=headers)

    bs = BS(html.text, 'html.parser')

    events = ['https://afisha.yandex.ru' + j['href'] for i in
              bs.find_all('div', class_='event events-list__item yandex-sans') for j in
              i.findChildren('a', recursive=True) if 'EventLink' in j['class'][0]]

    img = qrcode.make(choice(events))
    img.save('qrcodes/qr_event.png')


def generate_place():
    html = session.get('https://zen.yandex.ru/media/id/5e7b8daa7bdb6e1b170e5cd0/top35-glavnye-dostoprimechatelnosti-'
                       'kaliningrada-kuda-shodit-i-chto-posmotret-foto-s-opisaniem-5eb91546ce86a8785f6e0205',
                       headers=headers)

    url = 'https://yandex.ru/maps/22/kaliningrad/search/'

    bs = BS(html.text, 'html.parser')

    places = ['%20'.join(i.span.text.lower().split()[1:]) for i in
              bs.find_all('h3', class_='article-render__block article-render__block_underlined-text-enabled '
                                       'article-render__block_bold-italic-combination-enabled article-render_'
                                       '_block_h3') if i.span.text[0].isdigit()]

    url_places = [url + i + '/' for i in places]

    img = qrcode.make(choice(url_places))
    img.save('qrcodes/qr_place.png')

