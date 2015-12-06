# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class MeituItem(scrapy.Item):
	viewUrl = scrapy.Field()
	image = scrapy.Field()
	title = scrapy.Field()
	name = scrapy.Field()
	icon = scrapy.Field()
	likeCount = scrapy.Field()
	comment = scrapy.Field()

class Qiushi(scrapy.Item):
	icon = scrapy.Field()
	name = scrapy.Field()
	content = scrapy.Field()
	linkCount = scrapy.Field()
	commentCount = scrapy.Field()
	videoImage = scrapy.Field()
	videoUrl = scrapy.Field()

class Tudou(scrapy.Item):
	icon = scrapy.Field()
	name = scrapy.Field()
	videoUrl = scrapy.Field()
	area = scrapy.Field()

class Book(scrapy.Item):
	name = scrapy.Field()
	type = scrapy.Field()
	author = scrapy.Field()
	count = scrapy.Field()
	chapters = scrapy.Field()

class Meinv(scrapy.Item):
	title = scrapy.Field()
	icon = scrapy.Field()
	count = scrapy.Field()
	images = scrapy.Field()

class Joke(scrapy.Item):
	title = scrapy.Field()
	content = scrapy.Field()
	type = scrapy.Field()


