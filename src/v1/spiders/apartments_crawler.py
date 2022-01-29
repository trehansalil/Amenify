import scrapy
from src.common import link_extractor

class ApartmentsCrawlerSpider(scrapy.Spider):
    name = 'apartments_crawler'
    allowed_domains = ['www.apartments.com']
    start_urls = ['http://www.apartments.com/']

    def parse(self, response):
        pass
