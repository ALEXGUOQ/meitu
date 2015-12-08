# -*- coding: utf-8 -*-
import scrapy
import re

# 抓取17k电子书中全本免费的电子书
from meitu.items import Book


class Spider_17k(scrapy.Spider):
	name = "17k"

	start_urls=[
		'http://all.17k.com/lib/book/2_0_0_0_3_0_1_0_1.html',
	]

	dictUrl = 'http://all.17k.com'

	chapterUrl = "http://www.17k.com"

	index = 0

	#处理分类
	def parse(self, response):
		for eachType in response.xpath('//div[@class="fllist"]/div[1]/dl/dd'):
			for types in eachType.xpath('./a'):
				typeName = types.xpath('./@href').extract()
				if typeName:
					typeUrl = self.dictUrl + typeName[0]
					yield scrapy.Request(typeUrl,callback=self.handleType)

	#处理分页
	def handleType(self,response):
		nextPage = response.xpath('//div[@class="search-list"]/div[@class="page"]/text()').extract()
		pageCount = 0
		for page in nextPage:
			mode = re.compile(r'\d+')
			num = mode.findall(page.lstrip().strip().rstrip(','))
			if len(num):
				pageCount = num[0]
			else:
				del page

		nextPageUrl = response.xpath('//div[@class="search-list"]/div[@class="page"]/a[@class="on"]/@href').extract()
		nextPageUrl = nextPageUrl[0]
		if nextPageUrl:
			arr = nextPageUrl.split('_')
			arr.pop()

			subStr = ''
			for s in arr:
				subStr = subStr + s + "_"

			pageCount = int(pageCount)
			if pageCount:
				for pageIndex in range(1,(pageCount + 1)):
					pageUrl = subStr + str(pageIndex) +'.html'
					pageUrl = self.dictUrl + pageUrl
					yield scrapy.Request(pageUrl,callback=self.handlePages)

	# 处理书的基本信息
	def handlePages(self,response):
		for eachBook in response.xpath('//div[@class="main searchjg"]/div[@class="search-list"]/div[@class="alltable"]/table/tbody/tr'):
			book = Book()

			type = eachBook.xpath('./td[@class="td2"]/a/text()').extract()
			if type:
				type = type[0]
				book['type'] = type
			else:
				continue

			name = eachBook.xpath('./td[@class="td3"]/span/a/text()').extract()
			if name:
				name = name[0]
				book['name'] = name
			else:
				book['name'] = ''

			author = eachBook.xpath('./td[@class="td6"]/a/text()').extract()
			if author:
				author = author[0]
				book['author'] = author
			else:
				book['author'] = ''

			count = eachBook.xpath('./td[@class="td5"]/text()').extract()
			if count:
				count = count[0]
				book['count'] = count
			else:
				book['count'] = ''

			item_details_url = eachBook.xpath('./td[@class="td3"]/span/a/@rel').extract()
			if item_details_url:
				item_details_url = item_details_url[0]
				requestUrl = self.dictUrl + item_details_url
				yield scrapy.Request(requestUrl, callback=self.handleDictUrl, meta={'book': book})


	# 处理调整页面
	def handleDictUrl(self,response):
		book = response.meta['book']
		detailUrl = response.xpath('/html/body/div[@class="innerbut"]/a[@class="ts"]/@href').extract()

		if detailUrl:
			detailUrl = detailUrl[0]
			yield scrapy.Request(detailUrl,callback=self.handleChapters,meta={'book': book})

	# 获取章节
	def handleChapters(self,response):
		book = response.meta['book']
		book['chapters'] = []

		for eachChapter in response.xpath('//div[@class="directory_con"]/div'):
			for chapter in eachChapter.xpath('./ul/li'):
				name = chapter.xpath('./a/text()').extract()
				if name:
					name = name[0]

				url = chapter.xpath('./a/@href').extract()
				if url:
					url =self.chapterUrl + url[0]

				if name and url:
					book['chapters'].append({name:url})

		for content in book['chapters']:
			for contentUrl in content.values():
				yield scrapy.Request(contentUrl,self.handleContent,meta={'item':book})


	def handleContent(self,response):
		requestUrl = response.url
		book = response.meta['item']

		chapterContent = response.xpath('//div[@id="chapterContent"]/div[@id="chapterContentWapper"]/text()').extract()
		if chapterContent:
			chapterContent = chapterContent[0]

		for content in book['chapters']:
			for (k,v) in content.items():
				if v == requestUrl:
					content[k] = chapterContent

		self.index += 1
		if self.index == len(book['chapters']):
			self.index = 0
			return book


