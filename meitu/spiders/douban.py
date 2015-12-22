# # -*- coding: utf-8 -*-
# import scrapy
#
# # 抓取豆瓣电影TOP250
# from meitu.items import Douban
# import re
# from scrapy.selector import Selector
#
# class douban(scrapy.Spider):
# 	name = "douban"
#
# 	start_urls =['http://movie.douban.com/top250']
#
# 	url = 'http://movie.douban.com/top250'
#
# 	def parse(self, response):
# 		douban = Douban()
# 		selector = Selector(response)
# 		movices = selector.xpath('//div[@id="content"]/div[@class="grid-16-8 clearfix"]/div[@class="article"]/ol[@class="grid_view"]/li')
#
# 		for eachMovice in movices:
# 			rank = eachMovice.xpath('./div[@class="item"]/div[@class="pic"]/em/text()').extract()
# 			if rank:
# 				rank = rank[0]
# 			else:
# 				rank = ''
#
# 			movieIcon = eachMovice.xpath('./div[@class="item"]/div[@class="pic"]/a/img/@src').extract()
# 			if movieIcon:
# 				movieIcon = movieIcon[0]
# 			else:
# 				movieIcon = ''
#
# 			moviceTitle = ''
# 			for titles in eachMovice.xpath('./div[@class="item"]/div[@class="info"]/div[@class="hd"]/a/span'):
# 				title = titles.xpath('./text()').extract()
# 				if title:
# 					title = title[0]
# 					moviceTitle += title.encode('utf-8')
#
# 			if moviceTitle:
# 				moviceTitle = moviceTitle
# 			else:
# 				moviceTitle = ''
#
# 			director = eachMovice.xpath('./div[@class="item"]/div[@class="info"]/div[@class="bd"]/p/text()').extract()
# 			if director:
# 				director = director[0]
# 				p = re.compile('\s+')
# 				director = re.sub(p, '', director)
# 			else:
# 				director = ''
#
# 			comments = eachMovice.xpath('//div[@class="star"]/span[4]/text()').extract()
# 			if comments:
# 				comments = comments[0]
# 				comments = comments.encode('utf-8')
# 			else:
# 				comments = ''
#
# 			words = eachMovice.xpath('//p[@class="quote"]/span/text()').extract()
# 			if words:
# 				words = words[0].encode('utf-8')
# 			else:
# 				words = ''
#
# 			detailUrl = eachMovice.xpath('//div[@class="hd"]/a/@href').extract()
# 			if detailUrl:
# 				detailUrl = detailUrl[0]
# 			else:
# 				detailUrl = ''
#
# 			douban['rank'] = rank
# 			douban['icon'] = movieIcon
# 			douban['title'] = moviceTitle
# 			douban['director'] = director
# 			douban['comments'] = comments
# 			douban['quote'] = ""
# 			douban['detailUrl'] = ""
# 			yield douban
#
# 		nextPageUrl = response.xpath('//div[@class="paginator"]/span[@class="next"]/a/@href').extract()
# 		if nextPageUrl:
# 			nextPageUrl = nextPageUrl[0]
# 			requestUrl = self.url + nextPageUrl
# 			yield scrapy.Request(requestUrl,callback=self.parse)

#-*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
import re

from meitu.items import DoubanmovieItem


class Douban(CrawlSpider):
	name = "douban"

	start_urls = ['http://movie.douban.com/top250']

	url = 'http://movie.douban.com/top250'

	def parse(self,response):
		item = DoubanmovieItem()
		selector = Selector(response)
		Movies = selector.xpath('//div[@class="info"]')
		for eachMoive in Movies:
			title = eachMoive.xpath('div[@class="hd"]/a/span/text()').extract()
			fullTitle = ''
			for each in title:
				fullTitle += each
			movieInfo = eachMoive.xpath('div[@class="bd"]/p/text()').extract()

			star = eachMoive.xpath('div[@class="bd"]/div[@class="star"]/span[2]/text()').extract()
			if star:
				star = star[0]
			else:
				star = ''

			quote = eachMoive.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()
			#quote可能为空，因此需要先进行判断
			if quote:
				quote = quote[0]
			else:
				quote = ''

			item['title'] = fullTitle
			p = re.compile('\s+')
			movieInfo = ';'.join(movieInfo)
			movieInfo = re.sub(p, '', movieInfo)
			item['movieInfo'] = movieInfo
			item['star'] = star
			item['quote'] = quote
			yield item

		nextLink = selector.xpath('//span[@class="next"]/link/@href').extract()
		#第10页是最后一页，没有下一页的链接
		if nextLink:
			nextLink = nextLink[0]
			yield Request(self.url + nextLink,callback=self.parse)