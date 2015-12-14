from scrapy.crawler import CrawlerProcess

from meitu.spiders import Spider_joke
from meitu.spiders.Spider_jokeRanking import Spider_jokeRanking
from meitu.spiders.Spider_jokeType import Spider_jokeType

process = CrawlerProcess()
process.crawl(Spider_joke)
process.crawl(Spider_jokeRanking)
process.crawl(Spider_jokeType)
process.start()
