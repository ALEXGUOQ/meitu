# -*- coding: utf-8 -*-

import scrapy
import re

from meitu.items import Joke


class Spider_jokeType(scrapy.Spider):
	name = 'jokeType'

	start_urls =[
		'http://www.jokeji.cn/Keyword.htm',
	]

	baseUrl = 'http://www.jokeji.cn'

	def parse(self, response):
		links = response.xpath('//a[contains(@href, "/list")]')
		links.extract()

		for index, link in enumerate(links):
			args = (index, link.xpath('@href').extract(), link.xpath('text()').extract())
			type = args[2][0]

			url = self.baseUrl + args[1][0]

			yield scrapy.Request(url,callback=self.handlePages,meta={'type':type})

	def handlePages(self,response):
		type = response.meta['type']
		pageCount = 0
		for pages in response.xpath('//a[contains(@href, "keyword.asp?me_page=")]'):
			pageName = pages.xpath('./img/@alt').extract()
			if pageName:
				pageName = pageName[0]

				if pageName == "尾页".decode('utf-8'):
					pageUrl = pages.xpath('./@href').extract()[0]
					mode = re.compile(r'\d+')
					count = mode.findall(pageUrl)[0]
					pageCount = int(count)

		pageCount += 1
		for i in range(1,pageCount):
			pageUrl = self.baseUrl + "/keyword.asp?me_page=" + str(i)
			yield scrapy.Request(pageUrl,callback=self.handleJokes,meta={'type':type})

	def handleJokes(self,response):
		type = response.meta['type']
		for jokes in response.xpath('//table[contains(@background, "images/")]'):
			joke = Joke()
			joke['type'] = type
			title = jokes.xpath('./tr/td[2]/a[@class="main_14"]/text()').extract()[0]
			joke['title'] = title

			url = jokes.xpath('./tr/td[2]/a[@class="main_14"]/@href').extract()[0]
			requestUrl = self.baseUrl + url

			yield scrapy.Request(requestUrl,callback=self.handleContent,meta={'joke':joke})

	def handleContent(self,response):
		joke = response.meta['joke']

		joke['content'] = []
		for contents in response.xpath('//span[@id="text110"]/p'):
			content = contents.xpath('./text()').extract()
			if content:
				joke['content'].append(content[0])

		return joke
