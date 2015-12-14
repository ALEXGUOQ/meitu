# -*- coding: utf-8 -*-
import scrapy
from meitu.items import Qiushi

class Spider_qiushibaike(scrapy.Spider):
	name = "qiubai"

	start_urls = [
		'http://www.qiushibaike.com'
	]

	def parse(self, response):
		for eachType in  response.xpath('//div[@id="menu"]/a'):
			type = eachType.xpath('./@href').extract()
			requestUrl = self.start_urls[0] + type[0]
			yield scrapy.Request(requestUrl,callback=self.handleType)

	def handleType(self,response):
		for eachMunu in response.xpath('//div[@class="menu_list"]/ul/li/a'):
			menus = eachMunu.xpath('./@href').extract()
			menu = menus[0]
			requestUrl = self.start_urls[0] + menu
			yield scrapy.Request(requestUrl, callback = self.handleReponse)

	def handleReponse(self,response):
		for eachItem in response.xpath("//div[@class='article block untagged mb15']"):
			qiushi = Qiushi()
			icon = eachItem.xpath('./div[1]/a[1]/img/@src').extract()
			if icon:
				qiushi['icon'] = icon[0]
			else:
				continue

			name = eachItem.xpath('./div[1]/a[2]/h2/text()').extract()
			if name:
				qiushi['name'] = name[0]
			else:
				continue

			content = eachItem.xpath('./div[@class="content"]/text()').extract()
			if content:
				content = content[0]
				qiushi['content'] = content
			else:
				continue

			images = eachItem.xpath('./div[@class="thumb"]/a/img/@src').extract()
			if images:
				image = images[0]
				qiushi['image'] = image
			else:
				qiushi['image'] = ''

			likeCount = eachItem.xpath('./div[@class="stats"]/span[@class="stats-vote"]/i/text()').extract()
			if likeCount:
				qiushi['linkCount'] = likeCount[0]
			else:
				qiushi['linkCount'] = ''

			commentCount = eachItem.xpath('./div[@class="stats"]/span[@class="stats-comments"]/a/i/text()').extract()
			if commentCount:
				qiushi['commentCount'] = commentCount[0]
			else:
				qiushi['commentCount'] = ''

			videoImage = eachItem.xpath('./div[@class="video_holder"]/video/@poster').extract()
			if videoImage:
				videoImage = videoImage[0]
				qiushi['videoImage'] = videoImage

				videoUrl = eachItem.xpath('./div[@class="video_holder"]/video/source/@src').extract()
				if videoUrl:
					videoUrl = videoUrl[0]
					qiushi['videoUrl'] = videoUrl
				else:
					qiushi['videoUrl'] = ''
			else:
				qiushi['videoImage'] = ""
				qiushi['videoUrl'] = ''

			yield qiushi

		nextPage = response.xpath('//div[@class = "pagebar clearfix"]/div[1]/a[2]/@href').extract()
		if nextPage:
			nextPageUrl = self.start_urls[0] + nextPage[0]
			yield scrapy.Request(nextPageUrl, callback=self.handleReponse)