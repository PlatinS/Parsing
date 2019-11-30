# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst

class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    id_ = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    salary = scrapy.Field()
    s_min = scrapy.Field()
    s_max = scrapy.Field()
    source = scrapy.Field()