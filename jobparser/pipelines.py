# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client['vacancies']

    def process_item(self, item, spider):
        if spider.name == 'superjobru':
            try:
                item['s_min'] = item['salary'][0]
            except :
                item['s_min'] = None
            try:
                item['s_max'] = item['salary'][4]
            except :
                item['s_max'] = None
            str_sal = ''.join(item['salary'])
            item['salary'] = str_sal

        if spider.name == 'hhru':
            # Add for ItemLoader
            item ['source'] = 'hh.ru'

            try:
                item['s_min'] = item['s_min'][0]
            except :
                item['s_min'] = None
            try:
                item['s_max'] = item['s_max'][0]
            except :
                item['s_max'] = None
            str_sal = ''.join(item ['salary'])
            item ['salary'] = str_sal

        coll = self.db[spider.name]
        coll.update_one(item, {'$set': item}, upsert=True)
        return item