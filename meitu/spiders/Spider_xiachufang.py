# -*- coding: utf-8 -*-
import scrapy
import re

from meitu.items import Xiachufang, Greens


def removeSpace(content):
	p = re.compile('\s+')
	content = re.sub(p, '', content)
	return content

class Spider_xiachufang(scrapy.Spider):
	name = 'xiachufang'

	start_urls = [
		'http://www.xiachufang.com/category'
	]

	baseUrl = 'http://www.xiachufang.com'

	def parse(self, response):
		for eachType in response.xpath('//div[@class="cates-list clearfix has-bottom-border pb20 mb20"]'):
			item = Xiachufang()
			type = eachType.xpath('./div[@class="cates-list-info p5 m15 float-left"]/h3/text()').extract()
			if type:
				type = type[0]
				item['type'] = type
			else:
				continue

			icon = eachType.xpath('./div[@class="cates-list-info p5 m15 float-left"]/img/@src').extract()
			if icon:
				icon = icon[0]
				item['icon'] = icon
			else:
				continue

			item['subType'] = []

			subTypes = eachType.xpath('./div[@class="cates-list-all clearfix hidden"]/ul/li').extract()

			count = len(subTypes)
			index = 0
			for subType in subTypes:
				href = re.findall('(?<="/)[\s\S]*(?=/")',subType,re.M)
				name = re.findall('/">(.*?)</a',subType,re.M)
				name = name[0]
				href = self.baseUrl + '/' + href[0] + '/'
				yield  scrapy.Request(href,callback=self.hanleDetails,meta={'item':item,'subTypeName':name,'count':count,'index':index})
				index += 1

	def hanleDetails(self,response):
		item = response.meta['item']
		subTypeName = response.meta['subTypeName']
		count = response.meta['count']
		index = response.meta['index']

		nameTupe = {}
		lists = []
		for list in response.xpath('//ul[@class="list"]/li'):
			greens = Greens()
			title = list.xpath('./div/div[@class="info pure-u"]/p[@class="name"]/a/text()').extract()
			if title:
				title = title[0]
				greens['title'] = title
			else:
				continue

			icon = list.xpath('./div/div[@class="cover pure-u"]/a/img/@data-src').extract()
			if icon:
				icon = icon[0]
				greens['icon'] = icon
			else:
				continue

			detailUrl = list.xpath('./div/div[@class="info pure-u"]/p[@class="name"]/a/@href').extract()
			if detailUrl:
				detailUrl = detailUrl[0]
				greens['detail'] = detailUrl
			else:
				continue

			lists.append(greens)

		nameTupe = {subTypeName:lists}
		item['subType'].append(nameTupe)

		if index == count:
			return item
