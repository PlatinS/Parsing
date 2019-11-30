# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from avitoparser.items import AvitoparserItem
from scrapy.loader import ItemLoader

class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/rossiya/avtomobili/bmw/x3?cd=1']

    def parse(self, response:HtmlResponse):
        ads_links = response.xpath('//a[@class="item-description-title-link"]/@href').extract()
        for link in ads_links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=AvitoparserItem(), response=response)
        loader.add_css('title','h1.title-info-title span.title-info-title-text::text')
        loader.add_css('price','span.js-item-price::text')
        loader.add_xpath('parameters','//ul[contains(@class,"item-params-list")]//li[contains(@class,"item-params-list-item")]')
        loader.add_xpath('photos','//div[contains(@class,"gallery-img-wrapper")]//div[contains(@class,"gallery-img-frame")]/@data-url')
        yield loader.load_item()