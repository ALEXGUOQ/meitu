# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

def dbHandle():
	conn = pymysql.connect(
		host = 'localhost',
		user = 'root',
		passwd = '',
		db='joke',
		charset='utf8',
		use_unicode= False
	)
	return conn

class JokePipeLine(object):

	def process_item(self,item,spider):
		dbObject = dbHandle()
		cursor = dbObject.cursor()
		sql = "insert into joke.t_joke(title,type,content,tag,image,video) values (%s,%s,%s,%s,%s,%s)"

		text = ''
		for content in item['content']:
				text += content.strip()

		cursor.execute(sql, (item['title'],item['type'],text,item['tag'],item['image'],item['video']))
		dbObject.commit()

		return item