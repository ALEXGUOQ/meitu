# -*- coding: utf-8 -*-
import scrapy
from meitu.items import Joke

class Spider_zol_video(scrapy.Spider):
	name = 'zolVideo'

	start_urls = [
		'http://xiaohua.zol.com.cn/video/'
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

			joke['tag'] = 'video'

			if jokeType:
				joke['type'] = jokeType
			else:
				continue

			title = eachItem.xpath('./span[@class="article-title"]/a/text()').extract()
			if title:
				title = title[0]
				joke['title'] = title
			else:
				continue

			joke['image'] = ''
			joke['content'] = ''

			videoUrl = eachItem.xpath('./div[@class="article-commentbar articleCommentbar clearfix"]/a/@href').extract()
			if videoUrl:
				videoUrl = videoUrl[0]
				requestUrl = self.baseUrl + videoUrl
				yield scrapy.Request(requestUrl,callback=self.handleVideo,meta={'item':joke})

		nextPageUrl = response.xpath('//div[@class="page-box"]/div[@class="page"]/a[@class="page-next"]/@href').extract()
		if nextPageUrl:
			requestUrl = self.baseUrl + nextPageUrl[0]
			yield scrapy.Request(requestUrl,callback=self.handleType,meta={'jokeType':jokeType})

	def handleVideo(self,response):
		joke = response.meta['item']

		videoUrl = response.xpath('//div[@class="section article"]/div[@class="article-text"]/p/embed/@src').extract()
		if videoUrl:
			videoUrl = videoUrl[0]
		else:
			videoUrl = ''

		joke['video'] = videoUrl

		return joke


