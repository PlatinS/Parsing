# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
from pprint import pprint

class DataBasePipeline(object):
    def __init__(self):
        db = MongoClient('localhost', 27017)
        self.mongo_base = db.ads

    def process_item(self, item, spider):
        item['price'] = int(item['price'][0].replace(' ',''))
        d = {}
        for i in item['parameters']:
            p1 = i.find("label")
            p2 = i.find("/span")
            p3 = i.find("/li")
            PR = i[p1+7:p2-3]
            ZP = i[p2+6:p3-2]
            d[PR] = ZP
        item ['parameters'] = d

        coll = self.mongo_base[spider.name]
        coll.update_one(item, {'$set': item}, upsert=True)
        return item

class AvitoPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
       if item['photos']:
           for img in item['photos']:
               try:
                   yield scrapy.Request(img)
               except Exception as e:
                   print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
