# -*- coding: utf-8 -*-
import scrapy

#煎蛋网
from meitu.items import Jiandan


class Spider_jiandan(scrapy.Spider):
	name = "jiandan"

	start_urls = [
		"http://jandan.net"
	]

	def parse(self, response):
		for eachItem in response.xpath('//div[@id="content"]/div[@class="post f list-post"]'):
			jiandan = Jiandan()
			icon = eachItem.xpath('./div[@class="thumbs_b"]/a/img/@src').extract()
			if icon:
				icon = icon[0]
				jiandan['icon'] = self.start_urls[0] + icon
			else:
				jiandan['icon'] = ""

			title = eachItem.xpath('./div[@class="indexs"]/h2/a/text()').extract()
			if title:
				title = title[0]
				jiandan['title'] = title

			desc = eachItem.xpath('./div[@class="indexs"]/text()').extract()
			text = ''
			for eachDesc in desc:
				text += eachDesc.strip()
			jiandan['desc'] = text

			author = eachItem.xpath('./div[@class="indexs"]/div[@class="time_s"]/a[1]/text()').extract()
			if author:
				author = author[0]
				jiandan['author'] = author

			authorUrl = eachItem.xpath('./div[@class="indexs"]/div[@class="time_s"]/a[1]/@href').extract()
			if authorUrl:
				authorUrl = authorUrl[0]
				jiandan['authorUrl'] = authorUrl

			tag = eachItem.xpath('./div[@class="indexs"]/div[@class="time_s"]/a[@rel="tag"]/text()').extract()
			if tag:
				tag = tag[0]
				jiandan['tag'] = tag

			tagUrl = eachItem.xpath('./div[@class="indexs"]/div[@class="time_s"]/a[@rel="tag"]/@href').extract()
			if tagUrl:
				tagUrl = tagUrl[0]
				jiandan['tagUrl'] = tagUrl

			detail = eachItem.xpath('./div[@class="thumbs_b"]/a/@href').extract()
			if detail:
				detailUrl = detail[0]
				yield scrapy.Request(detailUrl,callback=self.handleDetails,meta={'item':jiandan})


	def handleDetails(self,response):
		jiandan = response.meta['item']

		content = response.xpath('//div[@id="content"]/div[@class="post f"]/p/text()').extract()
		text = ''
		for eachContent in content:
			text += eachContent.strip()
		jiandan['content'] = text

		return jiandan