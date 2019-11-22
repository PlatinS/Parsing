from lxml import html
import requests
from pprint import pprint
import datetime
from pymongo import MongoClient

LINK = 'https://mail.ru/?from=m'
LINK0 = 'https://mail.ru'
LINK_L = 'https://m.lenta.ru/'
LINK_L0 = 'https://m.lenta.ru'
LINK_Y = 'https://yandex.ru/'
headers = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

def parsing_mail(news):
    req = requests.get(LINK0, params = {'from': 'm'}, headers = headers)
    print('Код состояния ответа: ',req.status_code)
    if req.ok:
        root = html.fromstring(req.text)
        res_news = root.xpath('//div[@id="news-0"]')

        for i in res_news:
            #list_item = i.xpath('.//a[@class="list__item"]')
            list_item = i.xpath('.//a[contains (@class, "list__item")]')
            for p in list_item:
                news_data = {}
                href = p.xpath('.//@href')
                item = p.xpath('.//span[@class="list__item__title"]/text()')
                #pprint(news)
                #pprint(href)
                now = datetime.datetime.now()
                news_data['site'] = 'mail.ru'
                # На мобильной странице сайта нет даты новости. Берём текущую.
                news_data['date'] = now.strftime("%d-%m-%Y %H:%M")
                news_data['news'] = item[0]
                news_data['link'] = href[0]
                news.append(news_data)
    else:
        print("Ошибка ответа MAIL.RU")

def parsing_lenta(news):
    req = requests.get(LINK_L, headers = headers)
    print('Код состояния ответа: ',req.status_code)
    if req.ok:
        root = html.fromstring(req.text)
        res_news = root.xpath('//ul[@class="b-list b-list_top-7"]')
        for i in res_news:
            links = i.xpath('.//li[@class="b-list-item b-list-item_news"]')
            for p in links:
                news_data = {}
                href = p.xpath('.//a[@class="b-list-item__link"]/@href')
                #pprint(LINK_L0+href[0])
                item = p.xpath('.//span[@class="b-list-item__title"]/text()')
                #pprint(item[0])
                dtm = p.xpath('.//a[@class="b-list-item__link"]/span[@class="b-list-item__time"]/time/@datetime')
                #pprint(dtm[0].lstrip())

                news_data['site'] = 'lenta.ru'
                news_data['date'] = dtm[0].lstrip()
                news_data['news'] = item[0]
                news_data['link'] = LINK_L0+href[0]
                news.append(news_data)
    else:
        print("Ошибка ответа LENTA.RU")

def parsing_yandex(news):
    req = requests.get(LINK_Y, headers = headers)
    print('Код состояния ответа: ',req.status_code)
    if req.ok:
        root = html.fromstring(req.text)
        #res_data = root.xpath('//span[contains (@class, "datetime text_gray_yes i-bem")]/@data-bem')[0]
        res_news = root.xpath('//ol[contains (@class, "list news__list")]')
        for i in res_news:
            tag_li = i.xpath('.//li')
            for p in tag_li:
                news_data = {}
                item = p.xpath('.//a[1]/@aria-label')
                href = p.xpath('.//a[1]/@href')
                #pprint(item)
                #pprint(href)
                now = datetime.datetime.now()
                news_data['site'] = 'yandex.ru'
                news_data['date'] = now.strftime("%d-%m-%Y %H:%M")
                news_data['news'] = item[0]
                news_data['link'] = href[0]
                news.append(news_data)
    else:
        print("Ошибка ответа YANDEX.RU")

def to_mongodb(dict, coll):
    try:
        k = 0
        for data in dict:
            coll.update_one(data, {'$set': data}, upsert = True)
            k += 1
        res = f'Записано (обновлено) {k} записей.'
    except Exception  as e:
        print(e)
        res = 'Проблема при сохранении в MongoDB.\n'
    return res


def main():
    client = MongoClient('localhost', 27017)
    db = client['news']
    col_mail = db.mail
    col_lent = db.lenta
    col_yand = db.yandex

    # Новости на Mail.ru
    news_mail = []
    parsing_mail(news_mail)
    pprint(news_mail)
    to_mongodb(news_mail, col_mail)

    # Новости на Lenta.ru
    news_lenta = []
    parsing_lenta(news_lenta)
    pprint(news_lenta)
    to_mongodb(news_lenta, col_lent)

    # Новости на Yandex.ru
    news_yandex = []
    parsing_yandex(news_yandex)
    pprint(news_yandex)
    to_mongodb(news_yandex, col_yand)

if __name__ == '__main__':
    main()


