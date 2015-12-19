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
	tag = scrapy.Field() # 笑话的类型 txt 文本笑话 image : 趣图 video：搞笑视频
	image = scrapy.Field()
	video = scrapy.Field()

class Jiandan(scrapy.Item):
	icon = scrapy.Field()
	title = scrapy.Field()
	desc = scrapy.Field()
	author = scrapy.Field()
	authorUrl = scrapy.Field()
	tag = scrapy.Field()
	tagUrl = scrapy.Field()
	content = scrapy.Field()

class Baike(scrapy.Item):
	type = scrapy.Field()
	icon = scrapy.Field()
	title = scrapy.Field()
	content = scrapy.Field()

class Dog(scrapy.Item):
	name = scrapy.Field()
	alias = scrapy.Field()
	englishName = scrapy.Field()
	type = scrapy.Field()
	function = scrapy.Field()
	hair = scrapy.Field()
	height = scrapy.Field()
	weight = scrapy.Field()
	lifeTime = scrapy.Field()
	sourceArea = scrapy.Field()
	price = scrapy.Field()
	detail = scrapy.Field()
	FCIStandard = scrapy.Field()
	animType = scrapy.Field() # 动物的类型：dog：狗 cat: 猫

