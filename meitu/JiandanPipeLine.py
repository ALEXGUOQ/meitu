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
		db='jiandan',
		charset='utf8',
		use_unicode= False
	)
	return conn

class JiandanPipeLine(object):

	def process_item(self,item,spider):
		dbObject = dbHandle()
		cursor = dbObject.cursor()
		sql = "insert into jiandan.t_jiandan(icon,title,desc,tag,tagUrl,author,authorUrl,content) values (%s,%s,%s,%s,%s,%s,%s,%s)"
		cursor.execute(sql, (item['icon'],item['title'],item['desc'],item['tag'],item['tagUrl'],item['author'],item['authorUrl'],item['content']))
		dbObject.commit()
		return item