# -*- coding: utf-8 -*-
import scrapy

class Spider_jinritoutiao(scrapy.Spider):
	name = 'toutiao'

	start_urls =[
		'http://toutiao.com'
	]

	def parse(self, response):
		print response.url
		i = 0
		for eachItem in response.xpath('//div[@id="pagelet-feedlist"]/ul/li[@class="item clearfix"]'):
			print i
			i +=1