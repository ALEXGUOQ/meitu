# -*- coding: utf-8 -*-

import scrapy
import re

from meitu.items import Joke

class Spider_pengfuTxt(scrapy.Spider):
	name = 'pengfuTxt'

	start_urls = [
		'http://www.pengfu.com/zuijurenqi_1_1.html',
	]

	basePageUrl = 'http://www.pengfu.com/zuijurenqi_1_%s.html'
	pageCount = 0

	def parse(self, response):
		for eachTime in response.xpath('//div[@id="divIndex"]/ul/li/a'):
			timeUrl = eachTime.xpath('./@href').extract()
			if timeUrl:
				requestUrl = timeUrl[0]
				timeName = eachTime.xpath('./text()').extract()[0]
				yield scrapy.Request(requestUrl,callback=self.handleTimeType,meta={'type':timeName})

	def handleTimeType(self,response):
		type = response.meta['type']

		for pages in response.xpath('//div[@class="pageBox"]/div[@class="page"]/p/a'):
			pageName = pages.xpath('./text()').extract()
			if pageName:
				pageName = pageName[0]
				if pageName == '末页'.decode('utf-8'):
					pageNum = pages.xpath('./@href').extract()
					if pageNum:
						pageNum = pageNum[0]
						mode = re.compile(r'\d+')
						num = mode.findall(pageNum)
						self.pageCount = int(num[1]) + 1

		for i in range(1,self.pageCount):
			requestUrl = self.basePageUrl % i
			yield scrapy.Request(requestUrl,callback=self.handleJoke,meta={'type':type})

	def handleJoke(self,response):
		type = response.meta['type']

		for eachItem in response.xpath('//div[@class="main"]/div[@class="contentBox"]/div[@class="contL"]/div[@class="tieziBox"]'):
			joke = Joke()
			title = eachItem.xpath('./div[@class="contFont"]/div[@class="tieTitle"]/a/text()').extract()
			if title:
				title = title[0]
				joke['title'] = title
			else:
				continue

			content = eachItem.xpath('./div[@class="contFont"]/div[@class="imgbox"]/div[1]/text()').extract()
			if content:
				content = content[0]
				joke['content'] = content
			else:
				continue

			if type:
				joke['type'] = type
			else:
				continue

			joke['tag'] = 'txt'
			joke['image'] = ''
			joke['video'] = ''

			return joke


