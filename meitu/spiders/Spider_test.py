import scrapy
import re

def filter_tags(content,tag):
	re_tag = r'<%s(.*?)>(.*?)<\/%s>'%(tag,tag)
	dr = re.compile(re_tag,re.S)
	content = dr.sub('',content)
	dr = re.compile(r'</%s>'% tag ,re.S)
	content = dr.sub('',content)
	return content

class Spider_test(scrapy.Spider):
	name = "test"

	start_urls = [
		'http://www.baikezsw.com/wenhuazatan/7543.html'
	]

	def parse(self, response):
		detail = response.xpath('//div[@class="entry"]').extract()
		if detail:
			detail = detail[0].encode('utf-8')

			detail = filter_tags(detail,'div')
			detail = filter_tags(detail,'strong')
			detail = filter_tags(detail,'li')
			detail = filter_tags(detail,'ul')

			dr = re.compile(r'<br>',re.S)
			detail = dr.sub('',detail)

			dr = re.compile('<!--[^>]*-->')
			detail = dr.sub('',detail)

			detail = re.sub("<p.*?>", '',detail)
			detail = re.sub("<\/p>", '',detail)

			p = re.compile('\s+')
			detail = re.sub(p, '', detail)

			file = open('test.txt','wb')
			file.write(detail)

