import scrapy
from src.common.__init__ import link_extractor


class ApartmentsCrawlerSpider(scrapy.Spider):
    name = 'apartments_crawler'
    allowed_domains = ['www.apartments.com']
    start_urls = ['https://www.apartments.com/fremont-ca/']

    def parse(self, response):
        link_extractor(link=response.url)
        pass
