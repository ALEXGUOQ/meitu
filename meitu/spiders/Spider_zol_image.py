# -*- coding: utf-8 -*-
import scrapy
from meitu.items import Joke

class Spider_zol_image(scrapy.Spider):
	name = 'zolImage'

	start_urls = [
		'http://xiaohua.zol.com.cn/qutu/'
	]

	baseUrl = 'http://xiaohua.zol.com.cn'


	def parse(self, response):
		for eachType in response.xpath('//div[@class="filter"]/div[@class="filter-links clearfix"]/a'):
			type = eachType.xpath('./text()').extract()
			if type:
				type = type[0]
				typeUrl = eachType.xpath('./@href').extract()[0]
				requestUrl = self.baseUrl + typeUrl

				yield scrapy.Request(requestUrl,callback=self.handleType,meta={'jokeType':type})

	def handleType(self,response):
		jokeType = response.meta['jokeType']

		for eachItem in response.xpath('//ul[@class="article-list"]/li[@class="article-summary"]'):
			joke = Joke()

			joke['tag'] = 'image'

			if type:
				joke['type'] = jokeType
			else:
				continue

			title = eachItem.xpath('./span[@class="article-title"]/a/text()').extract()
			if title:
				title = title[0]
				joke['title'] = title
			else:
				continue

			imageUrl = eachItem.xpath('./div[@class="summary-text"]/p/a/img/@src').extract()
			if imageUrl:
				imageUrl = imageUrl[0]
			else:
				imageUrl = eachItem.xpath('./div[@class="summary-text"]/p/a/img/@loadsrc').extract()
				if imageUrl:
					imageUrl = imageUrl[0]

			if imageUrl:
				joke['image'] = imageUrl

			joke['content'] = ''
			joke['video'] = ''
			yield joke

		nextPageUrl = response.xpath('//div[@class="page-box"]/div[@class="page"]/a[@class="page-next"]/@href').extract()
		if nextPageUrl:
			requestUrl = self.baseUrl + nextPageUrl[0]
			yield scrapy.Request(requestUrl,callback=self.handleType,meta={'jokeType':jokeType})



