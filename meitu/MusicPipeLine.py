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

class MusicPipeLine(object):

	def process_item(self,item,spider):
		dbObject = dbHandle()
		cursor = dbObject.cursor()
		sql = "insert into joke.t_music(icon,title,meta,lists) values (%s,%s,%s,%s)"

		lists = ''
		for eachMusic in item['lists']:
			lists += eachMusic + '\t'

		cursor.execute(sql, (item['icon'],item['title'],item['meta'],lists))
		dbObject.commit()
		return item