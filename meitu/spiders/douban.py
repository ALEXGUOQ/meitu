# -*- coding: utf-8 -*-
import scrapy

# 抓取豆瓣电影TOP250
from meitu.items import Douban
import re

class douban(scrapy.Spider):
	name = "douban"

	start_urls =['http://movie.douban.com/top250']

	url = 'http://movie.douban.com/top250'

	def parse(self, response):
		for eachMovice in response.xpath('//div[@id="content"]/div[@class="grid-16-8 clearfix"]/div[@class="article"]/ol[@class="grid_view"]/li'):
			douban = Douban()

			rank = eachMovice.xpath('./div[@class="item"]/div[@class="pic"]/em/text()').extract()
			if rank:
				rank = rank[0]
				douban['rank'] = rank

			movieIcon = eachMovice.xpath('./div[@class="item"]/div[@class="pic"]/a/img/@src').extract()
			if movieIcon:
				movieIcon = movieIcon[0]
				douban['icon'] = movieIcon

			moviceTitle = ''
			for titles in eachMovice.xpath('./div[@class="item"]/div[@class="info"]/div[@class="hd"]/a/span'):
				title = titles.xpath('./text()').extract()
				if title:
					title = title[0]
					moviceTitle += title.encode('utf-8')

			if moviceTitle:
				douban['title'] = moviceTitle

			director = eachMovice.xpath('./div[@class="item"]/div[@class="info"]/div[@class="bd"]/p/text()').extract()
			if director:
				director = director[0]
				p = re.compile('\s+')
				director = re.sub(p, '', director)
				director = director.encode('utf-8')
				douban['director'] = director

			comments = eachMovice.xpath('//div[@class="star"]/span[4]/text()').extract()
			if comments:
				comments = comments[0]
				comments = comments.encode('utf-8')
				douban['comments'] = comments

			words = eachMovice.xpath('//p[@class="quote"]/span/text()').extract()
			if words:
				words = words[0].encode('utf-8')
				douban['quote'] = words
			else:
				douban['quote'] = ''

			detailUrl = eachMovice.xpath('//div[@class="hd"]/a/@href').extract()
			if detailUrl:
				detailUrl = detailUrl[0]
				douban['detailUrl'] = detailUrl
				yield douban

		nextPageUrl = response.xpath('//div[@class="paginator"]/span[@class="next"]/a/@href').extract()
		if nextPageUrl:
			nextPageUrl = nextPageUrl[0]
			requestUrl = self.url + nextPageUrl
			yield scrapy.Request(requestUrl,callback=self.parse)
