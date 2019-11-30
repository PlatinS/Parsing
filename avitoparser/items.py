# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst

def cleaner_photo(values):
    if values[:2] == '//':
        return f'http:{values}'
    return values

class AvitoparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    title = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field()
    parameters = scrapy.Field()
    photos = scrapy.Field(input_processor=MapCompose(cleaner_photo))
