# -*- coding: utf-8 -*-
import scrapy
import re

from meitu.items import Joke

class Spider_zol(scrapy.Spider):
	name = 'zolJoke'

	start_urls = [
		'http://xiaohua.zol.com.cn/new/'
	]

	baseUrl = 'http://xiaohua.zol.com.cn'

	def parse(self, response):
		for eachType in response.xpath('//div[@class="filter"]/div[@class="filter-links clearfix"]/a'):
			type = eachType.xpath('./text()').extract()
			if type:
				jokeType = type[0]
				typeUrl = eachType.xpath('./@href').extract()[0]
				requestUrl = self.baseUrl + typeUrl

				yield scrapy.Request(requestUrl,callback=self.handleType,meta={'jokeType':jokeType})

	def handleType(self,response):
		jokeType = response.meta['jokeType']

		for eachItem in response.xpath('//ul[@class="article-list"]/li[@class="article-summary"]'):
			joke = Joke()

			joke['tag'] = 'txt'

			if jokeType:
				joke['type'] = jokeType
			else:
				joke['type'] = ''
				continue

			title = eachItem.xpath('./span[@class="article-title"]/a/text()').extract()
			if title:
				title = title[0]
				joke['title'] = title
			else:
				continue

			contentUrl = eachItem.xpath('./span[@class="article-title"]/a/@href').extract()
			if contentUrl:
				detailUrl = self.baseUrl + contentUrl[0]

				yield scrapy.Request(detailUrl,callback=self.handleDetail,meta={'joke':joke})

		nextPageUrl = response.xpath('//div[@class="page-box"]/div[@class="page"]/a[@class="page-next"]/@href').extract()
		if nextPageUrl:
			requestUrl = self.baseUrl + nextPageUrl[0]
			yield scrapy.Request(requestUrl,callback=self.handleType,meta={'jokeType':jokeType})

	def handleDetail(self,response):
		joke = response.meta['joke']

		content = response.xpath('//div[@class="article-text"]').extract()
		if content:
			dr = re.compile(r'<[^>]+>',re.S)
			desc_nohtml = dr.sub('',content[0])
			desc_nohtml = desc_nohtml.replace('\t','').replace('\n','').replace(' ','')
			joke['content'] = desc_nohtml
		else:
			joke['content'] = ''

		joke['image'] = ''
		joke['video'] = ''
		return joke




