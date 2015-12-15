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

class BaikePipeLine(object):

	def process_item(self,item,spider):
		dbObject = dbHandle()
		cursor = dbObject.cursor()
		sql = "insert into joke.t_baike(title,type,content,icon) values (%s,%s,%s,%s)"

		try:
			cursor.execute(sql, (item['title'],item['type'],item['content'],item['icon']))
			dbObject.commit()
		except:
			dbObject.rollback()

		return item