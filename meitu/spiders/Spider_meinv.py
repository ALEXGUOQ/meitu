# -*- coding: utf-8 -*-
import scrapy
import re
from meitu.items import Meinv

class Spider_meinv(scrapy.Spider):
	name = 'meinv'

	start_urls = [
		'http://girl-atlas.com/'
	]

	def parse(self, response):
		for girls in response.xpath('//div[@class="column grid_6 grid"]'):
			girl = Meinv()
			girl['title'] = girls.xpath('./@title').extract()[0]

			icon = girls.xpath('./div[@class="inner"]/div[1]/a/@photo').extract()[0]
			girl['icon'] = icon

			count = girls.xpath('./div[@class="inner"]/div[@class="column grid_6 bar"]/div/a[1]/text()').extract()
			if count :
				mode = re.compile(r'\d+')
				num = mode.findall(count[0])
				girl['count'] = num[0]

			imagesUrl = girls.xpath('./div[@class="inner"]/div[1]/a/@href').extract()[0]
			yield scrapy.Request(imagesUrl,callback=self.hanldImages,meta={'girl':girl})

		page = response.xpath('//div[@class="paging column grid_12"]/a/@href').extract()
		pageUrl = self.start_urls[0] + page[0]
		print pageUrl
		yield scrapy.Request(pageUrl,callback=self.parse)


	def hanldImages(self,response):
		girl = response.meta['girl']

		girl['images'] = []
		for images in response.xpath('//ul[@class="slideview"]/li'):
			image = images.xpath('./img/@src').extract()
			if image:
				girl['images'].append(image[0])
			else:
				img = images.xpath('./img/@delay').extract()
				if img:
					print img[0]
		return girl


