# -*- coding: utf-8 -*-
import scrapy
from meitu.items import Qiushi

class Spider_qiushibaike(scrapy.Spider):
    name = "qiubai"

    start_urls = [
        'http://www.qiushibaike.com'
    ]

    def parse(self, response):
        for eachMunu in response.xpath('//div[@class="menu_list"]/ul/'):
            print "asdfasdf"

        # for eachItem in response.xpath("//div[@class='article block untagged mb15']"):
        #     qiushi = Qiushi()
        #     icon = eachItem.xpath('./div[1]/a[1]/img/@src').extract()
        #     if icon:
        #         qiushi['icon'] = icon[0]
        #     else:
        #         qiushi['icon'] = ''
        #
        #     name = eachItem.xpath('./div[1]/a[2]/h2/text()').extract()
        #     if name:
        #         qiushi['name'] = name[0]
        #     else:
        #         qiushi['name'] =''
        #
        #     content = eachItem.xpath('./div[@class="content"]/text()').extract()
        #     content = content[0]
        #     qiushi['content'] = content
        #
        #     likeCount = eachItem.xpath('./div[@class="stats"]/span[@class="stats-vote"]/i/text()').extract()
        #     qiushi['linkCount'] = likeCount[0]
        #
        #     commentCount = eachItem.xpath('./div[@class="stats"]/span[@class="stats-comments"]/a/i/text()').extract()
        #     qiushi['commentCount'] = commentCount[0]
        #
        #     videoImage = eachItem.xpath('./div[@class="video_holder"]/video/@poster').extract()
        #     if videoImage:
        #         videoImage = videoImage[0]
        #         qiushi['videoImage'] = videoImage
        #
        #         videoUrl = eachItem.xpath('./div[@class="video_holder"]/video/source/@src').extract()
        #         if videoUrl:
        #             videoUrl = videoUrl[0]
        #             qiushi['videoUrl'] = videoUrl
        #         else:
        #             qiushi['videoUrl'] = ''
        #     else:
        #         qiushi['videoImage'] = ""
        #         qiushi['videoUrl'] = ''
        #
        #     yield qiushi
        #
        # nextPage = response.xpath('//div[@class = "pagebar clearfix"]/div[1]/a[2]/@href').extract()
        # if nextPage:
        #     nextPageUrl = self.start_urls[0] + nextPage[0]
        #     yield scrapy.Request(nextPageUrl, callback=self.parse)

