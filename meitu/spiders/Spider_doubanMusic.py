# -*- coding: utf-8 -*-
import  scrapy
import re

from meitu.items import DoubanMusic

def removeSpace(content):
	p = re.compile('\s+')
	content = re.sub(p, '', content)
	return content

class Spider_doubanMusic(scrapy.Spider):
	name = "music"

	start_urls = [
		'http://music.douban.com/programmes'
	]

	def parse(self, response):
		# for eachType in response.xpath('//ul[@class="filter-tabs"]/li'):
		# 	typeName = eachType.xpath('./text()').extract()
		# 	if typeName:
		# 		typeName = typeName[0]
		# 		print typeName

		for eachMusics in response.xpath('//ul[@class="list-songlist slide-item"]/li[@class="songlist-item"]'):
			item = DoubanMusic()

			icon = eachMusics.xpath('./a/div[@class="songlist-info"]/div[@class="cover"]/img/@src').extract()
			if icon:
				icon = removeSpace(icon[0])
				item['icon'] = icon
			else:
				continue

			title = eachMusics.xpath('./a/div[@class="songlist-info"]/div[@class="cover"]/div[@class="girdle"]/div[@class="title"]/text()').extract()
			if title:
				title = removeSpace(title[0])
				item['title'] = title
			else:
				continue

			meta = eachMusics.xpath('./a/div[@class="songlist-info"]/div[@class="cover"]/div[@class="girdle"]/div[@class="meta"]/text()').extract()
			if meta:
				meta = removeSpace(meta[0])
				item['meta'] = meta
			else:
				continue

			detailUrl = eachMusics.xpath('./a/@href').extract()
			if detailUrl:
				detailUrl = removeSpace(detailUrl[0])
				yield scrapy.Request(detailUrl,callback=self.handleDetail,meta={'item':item})

	def handleDetail(self,response):
		item = response.meta['item']

		item['lists'] = []

		for musicInfos in response.xpath('//*[@id="songlist"]/li'):
			title = musicInfos.xpath('./div[@class="song-item"]/div[@class="song-info "]/span[2]/text()').extract()
			if title:
				title = title[0]
				item['lists'].append(title)

		return item