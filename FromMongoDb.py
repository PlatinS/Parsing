from pprint import pprint
from pymongo import MongoClient

def main():
    client = MongoClient('localhost', 27017)
    db = client['vacancies']
    sj = db.sj
    hh = db.hh

    print('Введите минимальную зарплату для сайта SuperJob.ru: ')
    min_sal = input()
    res = sj.find({ 'salary_min': {'$gte': int(min_sal) } })
    for i in res:
        pprint(i)

    print('Введите минимальную зарплату для сайта HH.ru: ')
    min_sal = input()
    res = hh.find({ 'salary_min': {'$gte': int(min_sal) } })
    for i in res:
        pprint(i)

if __name__ == '__main__':
    main()