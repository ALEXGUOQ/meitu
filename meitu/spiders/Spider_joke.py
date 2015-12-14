# -*- coding: utf-8 -*-

import scrapy
from meitu.items import Joke
import re

# 抓取笑话
class Spider_joke(scrapy.Spider):
	name = 'joke'

	start_urls = [
		'http://www.jokeji.cn/list.htm',
	]

	baseUrl = 'http://www.jokeji.cn'

	def parse(self, response):
		count = 0
		for pages in response.xpath('//div[@class="next_page"]/a'):
			pageName = pages.xpath('./text()').extract()
			if pageName:
				if pageName[0] == '尾页'.decode('utf-8'):
					pageCount = pages.xpath('./@href').extract()
					mode = re.compile(r'\d+')
					pageCount = mode.findall(pageCount[0])[0]
					count = int(pageCount) + 1

		for i in range(1,count):
			pageUrl = self.baseUrl + '/list_' + str(i) + '.htm'

			yield scrapy.Request(pageUrl,callback=self.hanldPages)

	def hanldPages(self,response):
		for jokes in response.xpath('//div[@class="list_title"]/ul/li'):
			joke = Joke()
			joke['type'] = '最新笑话'.decode('utf-8')
			title = jokes.xpath('./b/a/text()').extract()
			if title:
				joke['title'] = title[0]
			else:
				continue

			contentUrl = jokes.xpath('./b/a/@href').extract()
			if contentUrl:
				requestUrl = self.baseUrl + contentUrl[0]
				yield scrapy.Request(requestUrl,callback=self.handleContent,meta={'joke':joke})
			else:
				continue

	def handleContent(self,response):
		joke = response.meta['joke']
		joke['content'] = []

		content = response.xpath('//span[@id="text110"]').extract()
		if content:
			content = content[0]
			lists = re.findall(r"<p>(.*?)</p>",content,re.I)
			joke['content'] = lists
			return joke


