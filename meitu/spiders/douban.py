# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from meitu.items import MeituItem

# 抓取豆瓣电影TOP250
class douban(CrawlSpider):
    name = "douban"

    start_urls =['http://movie.douban.com/top250']

    url = 'http://movie.douban.com/top250'

    def parse(self, response):
        item = MeituItem()
        selector = Selector(response)

        movies = selector.xpath('//div[@class="info"]').extract()
        for eachMovice in movies:
            titles = eachMovice.xpath('div[@class="hd"]/a/span/text()')
            fullTitle = ''
            for each in titles:
                fullTitle += each

            print fullTitle
