# -*- coding: utf-8 -*-

import scrapy

class Spider_baike(scrapy.Spider):
	name = "baike"

	start_urls = [
		'http://www.baikezsw.com/jiajizhuangxiu/',
	]

	def parse(self, response):
		for eachType in response.xpath('//*[@id="menu-main"]/li[@class="menu-item mega-menu menu-item-type-taxonomy mega-menu menu-item-object-category mega-menu menu-item-has-children parent-list"]'):
			title = eachType.xpath('./a/text()').extract()
			if title:
				title = title[0]
				print title

			print eachType.xpath('//ul[contains(@class,"sub-menu")]').extract()

			# print eachType.xpath('//ul[@class="sub-menu"]/li').extract()
			#
			# for subType in eachType.xpath('./div/ul/li').extract():
			# 	print subType.xpath('./a/text()').extract()

			# for subType in eachType.xpath('./div[@class="mega-menu-block"]/ul[@class="sub-menu"]/li').extract():
			# 	subTypeName = subType.xpath('./a/text()').extract()
			# 	print subTypeName
			# 	if subTypeName:
			# 		subTypeName = subTypeName[0]
			# 		print title + "====" + subTypeName
