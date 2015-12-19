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

class DogPipeLine(object):

	def process_item(self,item,spider):
		dbObject = dbHandle()
		cursor = dbObject.cursor()

		englishName = ''
		if item['englishName']:
			englishName = item['englishName']
		else:
			item['englishName'] = ''

		hair = ''
		if item['hair']:
			hair = item['hair']
		else:
			hair = ''

		FCIStandard = ''
		if item['FCIStandard']:
			FCIStandard = item['FCIStandard']


		sql = "insert into joke.t_dog(name,alias,englishName,type,function,hair,height,weight,lifeTime,sourceArea,price,detail,FCIStandard) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		cursor.execute(sql, (item['name'],item['alias'],englishName,item['type'],item['function'],hair,item['height'],item['weight'],item['lifeTime'],item['sourceArea'],item['price'],item['detail'],FCIStandard))
		dbObject.commit()
		return item