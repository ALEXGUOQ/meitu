# -*- coding: utf-8 -*-

import scrapy
import re

from meitu.items import Baike

class Spider_baike(scrapy.Spider):
	name = "baike"

	start_urls = [
		'http://www.baikezsw.com/jijiashenghuo/',
	]

	def parse(self, response):
		for eachType in response.xpath('//*[@id="menu-main"]/li[@class="menu-item mega-menu menu-item-type-taxonomy mega-menu menu-item-object-category mega-menu menu-item-has-children parent-list"]'):
			title = eachType.xpath('./a/text()').extract()
			if title:
				title = title[0]

			for subType in eachType.xpath('./div[@class="mega-menu-block"]/ul[@class="sub-menu"]/li'):
				subTypeName = subType.xpath('./a/text()').extract()
				if subTypeName:
					subTypeName = subTypeName[0]

				subTypeUrl = subType.xpath('./a/@href').extract()
				if subTypeUrl:
					subTypeUrl = subTypeUrl[0]
					yield scrapy.Request(subTypeUrl,callback=self.handleItem,meta={'type':subTypeName})

	def handleItem(self,response):
		subType = response.meta['type']

		for eachItem in response.xpath('//div[@id="main-content"]/div[@class="content"]/div[@class="post-listing"]/article[@class="item-list"]'):
			baike = Baike()

			if subType:
				baike['type'] = subType

			title = eachItem.xpath('./h2/a/text()').extract()
			if title:
				title = title[0]
				baike['title'] = title
			else:
				continue

			icon = eachItem.xpath('./div[@class="post-thumbnail"]/a/img/@src').extract()
			if icon:
				icon = icon[0]
				baike['icon'] = icon
			else:
				continue

			detailUrl = eachItem.xpath('./h2/a/@href').extract()
			if detailUrl:
				detailUrl = detailUrl[0]

				yield scrapy.Request(detailUrl,callback=self.handleDetail,meta={'item':baike})

		for eachPage in response.xpath('//div[@class="pages"]/li'):
			pageName = eachPage.xpath('./a/text()').extract()
			nextPageUrl = eachPage.xpath('./a/@href').extract()

			if pageName:
				pageName = pageName[0]

				if pageName == '下一页'.decode('utf-8'):
					if nextPageUrl:
						nextPageUrl = nextPageUrl[0]

						url = response.url
						urlArrs = url.split('list_')
						requestUrl = urlArrs[0] + nextPageUrl
						yield scrapy.Request(requestUrl,callback=self.handleItem,meta={'type':subType})

	def handleDetail(self,response):
		baike = response.meta['item']

		detail = response.xpath('//div[@class="post-inner"]/div[@class="entry"]').extract()
		if detail:
			dr = re.compile(r'<[^>]+>',re.S)
			desc_nohtml = dr.sub('',detail[0])
			p = re.compile('\s+')
			desc_nohtml = re.sub(p, '', desc_nohtml)

			p = re.compile('(?<=[/*])[\s\S]*(?=";)')
			desc_nohtml = re.sub(p, '', desc_nohtml)

			desc_nohtml = re.sub('/";', '', desc_nohtml)

			baike['content'] = desc_nohtml
			return baike
