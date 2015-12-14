import scrapy

class Spider_jd(scrapy.Spider):
	name = 'jd'

	start_urls = [
		'http://jandan.net',
	]

	def parse(self, response):
		for eachItem in response.xpath('//div[@id="content"]/div[@class="post f list-post"]'):
			icon = eachItem.xpath('./div[@class="thumbs_b"]/a/img/@src').extract()
			print icon
			if icon:
				print "icon =" + icon[0]
			else:
				print eachItem
				print 'no'


