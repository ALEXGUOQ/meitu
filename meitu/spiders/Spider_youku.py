import scrapy

from meitu.items import Tudou


class Spider_youku(scrapy.Spider):
	name = 'youku'

	start_urls=[
		'http://www.youku.com/v_olist/c_96_a__s_1_d_1.html.html',
	]

	pageUrl = 'http://www.youku.com'

	def parse(self, response):
		for eachArea in response.xpath('//*[@id="filter"]/div[@class="yk-filter-panel"]/div[2]/ul/li'):
			area = eachArea.xpath('./a/@href').extract()
			if area:
				area = area[0]
			else:
				area = self.start_urls[0]

			yield scrapy.Request(area, callback=self.handleArea)

	def handleArea(self,response):
		for eachMovice in response.xpath('//div[@class="yk-col3"]'):
			icon = eachMovice.xpath('./div/div[@class="p-thumb"]/img/@src').extract()
			icon = icon[0]

			name = eachMovice.xpath('./div/div[@class="p-link"]/a/@title').extract()
			name = name[0]

			moviceUrl = eachMovice.xpath('./div/div[@class="p-meta pa"]/div[@class="p-meta-title"]/a/@href').extract()
			moviceUrl = moviceUrl[0]

			movice = Tudou()
			movice['icon'] = icon
			movice['name'] = name
			movice['videoUrl'] = moviceUrl

			yield movice

		nextPage = response.xpath('//*[@id="listofficial"]/div[@class="yk-pager"]/ul/li[@class="next"]/a/@href').extract()
		if nextPage:
			nextpageUrl = self.pageUrl + nextPage[0]
			yield scrapy.Request(nextpageUrl,callback=self.handleArea)
