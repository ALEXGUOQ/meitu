import scrapy
import re

from meitu.items import Dog


class Spider_dog(scrapy.Spider):
	name = 'dog'

	start_urls = [
		"http://m.ttpet.com",
	]

	def parse(self, response):
		for types in response.xpath('//dd[@id="quanzhong"]/dl[@class="breed_list"]/dd'):
			detailUrl = types.xpath('./a/@href').extract()
			if detailUrl:
				detailUrl = detailUrl[0]
				requestUrl = self.start_urls[0] + detailUrl
				yield scrapy.Request(requestUrl,callback=self.getDetails,meta={'type':'dog'})

		for maoTypes in response.xpath('//*[@id="maomi"]/dl/dd'):
			maomiDetailUrl = maoTypes.xpath('./a/@href').extract()
			if maomiDetailUrl:
				maomiRequestUrl = self.start_urls[0] + maomiDetailUrl[0]
				yield scrapy.Request(maomiRequestUrl,callback=self.getDetails,meta={'type':'cat'})

	def getDetails(self,response):
		animType = response.meta['type']

		dog = Dog()

		if animType:
			dog['animType'] = animType
		else:
			return

		details = response.xpath('/html/body/main/article/section[2]/dl/dd').extract()
		if details:
			dog['name'] = filterHtmlTag(details[0],'dd')
			dog['alias'] = filterHtmlTag(details[1],'dd')
			dog['englishName'] = filterHtmlTag(details[2],'dd')
			dog['type'] = filterHtmlTag(details[3],'dd')
			dog['function'] = filterHtmlTag(details[4],'dd')
			dog['hair'] = filterHtmlTag(details[5],'dd')
			dog['height'] = filterHtmlTag(details[6],'dd')
			dog['weight'] = filterHtmlTag(details[7],'dd')
			dog['lifeTime'] = filterHtmlTag(details[8],'dd')
			dog['sourceArea'] = filterHtmlTag(details[9],'dd')
			dog['price'] = filterHtmlTag(details[10],'dd')
			dog['FCIStandard'] = ''

		desc = response.xpath('/html/body/main/dl[1]/db/a/@href').extract()
		if desc:
			requestUrl = self.start_urls[0] + desc[0]
			yield scrapy.Request(requestUrl,callback=self.getDescInfo,meta={'item':dog})

		# FCIDetail = response.xpath('/html/body/main/dl[2]/db/a/@href').extract()
		# if FCIDetail:
		# 	FCIDetailUrl = self.start_urls[0] + FCIDetail[0]
		# 	yield scrapy.Request(FCIDetailUrl,callback=self.getFCIDetails,meta={'item':dog})

	def getFCIDetails(self,response):
		dog = response.meta['item']
		details = response.xpath('/html/body/main/article/section[2]').extract()
		if details:
			desc = details[0]
			dr = re.compile(r'<div class="cjj_next">(.*?)<\/div>',re.S)
			desc = dr.sub('',desc)
			dr = re.compile(r'<[^>]+>',re.S)
			desc = dr.sub('',desc)
			desc = desc.encode('utf-8')
			p = re.compile('\s+')
			desc = re.sub(p, '', desc)
			dog['FCIStandard'] = desc
		else:
			dog['FCIStandard'] = ''
		return dog

	def getDescInfo(self,response):
		dog = response.meta['item']

		desc = response.xpath('//section[@class="cjj_inf"]').extract()
		if desc:
			desc = desc[0]
			dr = re.compile(r'<div class="cjj_next">(.*?)<\/div>',re.S)
			desc = dr.sub('',desc)
			dr = re.compile(r'<[^>]+>',re.S)
			desc = dr.sub('',desc)
			desc = desc.encode('utf-8')
			p = re.compile('\s+')
			desc = re.sub(p, '', desc)
			dog['detail'] = desc
		else:
			dog['detail'] = ''
		yield dog


def filterHtmlTag(content,tag):
	content = re.sub("<%s.*?>" % tag, '',content)
	content = re.sub("<\/%s>" % tag, '',content)
	return content
