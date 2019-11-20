from bs4 import BeautifulSoup as bs
import requests
import lxml
import time
import pandas as pd
from pprint import pprint

headers = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
LINK_SJ = 'https://www.superjob.ru'
LINK_SSJ = 'https://www.superjob.ru/vacancy/search/'
LINK_HH0 = 'https://hh.ru'
LINK_HH = 'https://hh.ru/search/vacancy?only_with_salary=true&area=1&st=searchVacancy&text='
cur = {'RUR': 1, 'USD': 63.7, 'EUR': 70.5}

def input_vac():
    print('Введите вакансию: ')
    vacancy = input()
    print('Введите количество страниц сайта: ')
    num_str = input()
    return vacancy.replace(' ', '+'), num_str

def parameters(vacancy):
    parameters = {
        'User-Agent': AGENT,
        'keywords': vacancy,
        'payment_defined': 1,
        'geo%5Bc%5D%5B0%5D': 1
    }
    return parameters

def req_sj(link, vac, flag):
    if flag == 1:
        req = requests.get(link, parameters(vac))
    else:
        req = requests.get(link, headers = headers)

    #print('Superjob.ru - Код ответа: ', req.status_code)
    if req.ok:
        html = req.text
    else:
        html = None

    return html

def req_hh(link):
    req = requests.get(link, headers = headers)

    #print('hh.ru - Код ответа: ', req.status_code)
    if req.ok:
        html = req.text
    else:
        html = None

    return html

def salary_sj(str):
    po, do, ot, ru = 0, 0, 0, 0

    po = str.find("—")
    do = str.find("до")
    ot = str.find("от")
    ru = str.find("₽")
    if po >= 0:
        s1 = str[0:po]
        s2 = str[po + 1:ru]
    elif do >= 0:
        s2 = str[do + 3:ru]
        s1 = s2
    elif ot >= 0:
        s1 = str[ot + 3:ru]
        s2 = s1
    else:
        s1 = str[0:ru]
        s2 = s1
    
    sl1 = int(s1.replace(' ',''))
    sl2 = int(s2.replace(' ',''))
    return sl1, sl2

def salary_hh(href_link):
    s1, s2 = None, None
    html = req_hh(href_link)
    if html is None:
        print("Ошибка ответа внутр. стр. HH.RU")
    else:
        #time.sleep(1)
        parsed_html = bs(html, 'lxml')
        v_div = parsed_html.find('div', {'class': "vacancy-title"})
        try:
            currency = v_div.find('meta', {'itemprop': "currency"})['content']
            slr_val = v_div.find('meta', {'itemprop': "value"})
            slr_min = v_div.find('meta', {'itemprop': "minValue"})
            slr_max = v_div.find('meta', {'itemprop': "maxValue"})
            curs = cur.get(currency, 1)
            if slr_val is not None:
                s1 = int(slr_val['content']) * curs
            if slr_min is not None:
                s1 = int(slr_min['content']) * curs
            if slr_max is not None:
                s2 = int(slr_max['content']) * curs
        except Exception  as e:
            print(e)
    return s1, s2

def parsing_sj(html, vacancies):
    parsed_html = bs(html, 'lxml')
    v_list = parsed_html.find_all('div',{'class':'_3syPg _3P0J7 _9_FPy'})
    link_next = parsed_html.find('a', {'class': 'icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-dalshe'})

    for v in v_list:
        vac_data={}
        try:
            # Должность
            name_div = v.find('div', {'class': '_3mfro CuJz5 PlM3e _2JVkc _3LJqf'}).getText()
            # Зарплата
            summ_span = v.find('span', {'class': "_3mfro _2Wp8I f-test-text-company-item-salary PlM3e _2JVkc _2VHxz"}).getText()
            a_all = v.find_all('a')
            href_a = a_all[0]['href']
            # Ссылка на страницу вакансии
            href_link = LINK_SJ + href_a
            # Работадатель
            comp = a_all[1].getText()
            # Когда опубликована вакансия
            time_div = v.find('span', {'class': '_3mfro _9fXTd _2JVkc _3e53o _3Ll36'})
            # Город
            town_div = time_div.findNextSiblings()[0].getText()

            vac_data['site'] = 'superjob.ru'
            vac_data['name'] = name_div
            str_salary = summ_span.replace('\xa0',' ')
            sum_min, sum_max = salary_sj(str_salary)
            vac_data['salary_min'] = sum_min
            vac_data['salary_max'] = sum_max
            vac_data['salary'] = str_salary
            vac_data['firma'] = comp
            vac_data['city'] = town_div
            vac_data['link'] = href_link
            vacancies.append(vac_data)
        except Exception  as e:
            print(e)
    return link_next

def parsing_hh(html, vacancies):
    parsed_html = bs(html, 'lxml')
    v_list = parsed_html.find('div', {'class': 'vacancy-serp'})
    link_next = parsed_html.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})

    for v in v_list:
        vac_data = {}
        try:
            teg_a = v.find('a', {'class': 'bloko-link HH-LinkModifier'})
            name_div = teg_a.getText()
            href_link = teg_a['href']
            summ_span = v.find('div', {'class': "vacancy-serp-item__compensation"}).getText().replace('\xa0', ' ')
            comp = v.find('a', {'class': 'HH-AnonymousIndexAnalytics-Recommended-Company'}).getText()
            town = v.find('span', {'class': "vacancy-serp-item__meta-info"}).getText()
            sum_min, sum_max = salary_hh(href_link)
            vac_data['site'] = 'hh.ru'
            vac_data['name'] = name_div
            vac_data['salary_min'] = sum_min
            vac_data['salary_max'] = sum_max
            vac_data['salary'] = summ_span
            vac_data['firma'] = comp
            vac_data['city'] = town
            vac_data['link'] = href_link
            vacancies.append(vac_data)
        except Exception:
            pass
    return link_next

def main():
    vacancies = []
    vac, nst = input_vac()
    print("Поиск вакансий: ", vac, " на ", nst, " страницах")

    # Поиск на сайте SuperJob.RU
    html = req_sj(LINK_SSJ, vac, 1)
    if html is None:
        print("Ошибка ответа SuperJob.RU")
        link_next = None
    else:
        # Первая страница
        print("Поиск вакансий на SuperJob.RU")
        print('SuperJob.RU - страница: 1')
        link_next = parsing_sj(html, vacancies)

    # Следующие страницы SUPERJOB.RU
    for st in range(1, int(nst)):
        if link_next is None:
            print("На сайте SUPERJOB.RU нет следующей страницы")
            break
        else:
            print('SUPERJOB.RU - страница:', st+1)
            #pprint(LINK_SJ + link_next['href'])
            time.sleep(2)
            html = req_sj(LINK_SJ + link_next['href'], vac, 2)
            link_next = parsing_sj(html, vacancies)

    # Поиск на сайте HH.RU
    html = req_hh(LINK_HH+vac)
    if html is None:
        print("Ошибка ответа HH.RU")
        link_next_hh = None
    else:
        # Первая страница
        print("Поиск вакансий на HH.RU")
        print('HH.RU - страница: 1')
        link_next_hh = parsing_hh(html, vacancies)

    # Следующие страницы HH.RU
    for st in range(1, int(nst)):
        if link_next_hh is None:
            print("На сайте HH.RU нет следующей страницы")
            break
        else:
            print('HH.RU - страница:', st + 1)
            #pprint(LINK_HH0+link_next_hh['href'])
            time.sleep(2)
            html = req_hh(LINK_HH0+link_next_hh['href'])
            link_next_hh = parsing_hh(html, vacancies)

    df = pd.DataFrame(vacancies)
    df.to_csv('vacancies.csv', index=False, float_format = '%.0f')

if __name__ == '__main__':
    main()