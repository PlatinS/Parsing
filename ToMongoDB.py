import pandas as pd
from pymongo import MongoClient

def to_mongodb(dict, coll):
    try:
        k = 0
        for data in dict:
            coll.update_one(data, {'$set': data}, True)
            k += 1
        res = f'Записано (обновлено) {k} вакансий.'
    except Exception  as e:
        print(e)
        res = 'Проблема при сохранении в MongoDB.\n'
    return res

def main():
    client = MongoClient('localhost', 27017)
    db = client['vacancies']
    coll_sj = db.sj
    coll_hh = db.hh

    df = pd.read_csv('vacancies.csv', index_col=0)
    df_hh = df.query("site == 'hh.ru'").copy()
    df_sj = df.query("site == 'superjob.ru'").copy()

    answer = to_mongodb(df_sj.to_dict('records'), coll_sj)
    print(f'Коллекция SJ: {answer}')

    answer = to_mongodb(df_hh.to_dict('records'), coll_hh)
    print(f'Коллекция HH: {answer}')

if __name__ == '__main__':
    main()
