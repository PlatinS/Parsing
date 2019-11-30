# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
from scrapy.loader import ItemLoader

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?only_with_salary=true&area=1&st=searchVacancy&text=python']

    def parse(self, response):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)
        vacancy = response.css('div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header a.bloko-link::attr(href)').extract()
        for link in vacancy:
            yield response.follow(link, self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=JobparserItem(), response=response)
        #vac = response.xpath('//div[contains(@class,"vacancy-title")]//h1[@class="header"]//text()').extract()
        loader.add_xpath('name','//div[contains(@class,"vacancy-title")]//h1[@class="header"]//text()')
        #salary = response.css('div.vacancy-title p.vacancy-salary::text').extract()
        loader.add_css('salary', 'div.vacancy-title p.vacancy-salary::text')
        try:
            #sal_min = response.css('div.vacancy-title meta[itemprop="minValue"]::attr(content)').extract()
            loader.add_css('s_min', 'div.vacancy-title meta[itemprop="minValue"]::attr(content)')
        except:
            #sal_min = response.css('div.vacancy-title meta[itemprop="value"]::attr(content)').extract()
            loader.add_css('s_min', 'div.vacancy-title meta[itemprop="value"]::attr(content)')
        try:
            #sal_max = response.css('div.vacancy-title meta[itemprop="maxValue"]::attr(content)').extract()
            loader.add_css('s_max', 'div.vacancy-title meta[itemprop="maxValue"]::attr(content)')
        except:
            #sal_max = response.css('div.vacancy-title meta[itemprop="value"]::attr(content)').extract()
            loader.add_css('s_max', 'div.vacancy-title meta[itemprop="value"]::attr(content)')

        #link = response.css('div.bloko-column_xs-4 div[itemscope="itemscope"] meta[itemprop="url"]::attr(content)').extract()
        loader.add_css('link', 'div.bloko-column_xs-4 div[itemscope="itemscope"] meta[itemprop="url"]::attr(content)')

        #yield JobparserItem(name=vac[0], salary=salary, s_min=sal_min, s_max=sal_max, link=link[0], source='hh.ru')
        yield loader.load_item()