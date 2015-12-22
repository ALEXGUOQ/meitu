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

class DoubanPipeLine(object):

	def process_item(self,item,spider):
		dbObject = dbHandle()
		cursor = dbObject.cursor()
		sql = "insert into joke.t_doubanMovice(title,movieInfo,star,quote) values (%s,%s,%s,%s)"
		cursor.execute(sql, (item['title'],item['movieInfo'],item['star'],item['quote']))
		dbObject.commit()
		return item

		# dbObject = dbHandle()
		# cursor = dbObject.cursor()
		# sql = "insert into joke.t_movice(rank,icon,title,director,quote,comments,detailUrl) values (%s,%s,%s,%s,%s,%s,%s)"
		# cursor.execute(sql, (item['rank'],item['icon'],item['title'],item['director'],item['quote'],item['comments'],item['detailUrl']))
		# dbObject.commit()
		# return item