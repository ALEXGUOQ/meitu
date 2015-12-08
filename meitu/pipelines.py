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
		db='books',
		charset='utf8',
		use_unicode= False
	)
	return conn

class BookPipeline(object):

	def process_item(self, item, spider):
		dbObject = dbHandle()
		cursor = dbObject.cursor()
		sql = "insert into books.book (name,type,author,count,chapters) values (%s,%s,%s,%s,%s)"

		text = ''
		for content in item['chapters']:
			for value in content.values():
				text += value
		cursor.execute(sql, (item['name'],item['type'],item['author'],item['count'],text))
		dbObject.commit()
		return item
