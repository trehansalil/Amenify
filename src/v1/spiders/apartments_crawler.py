import scrapy
from src.common import link_extractor


class ApartmentsCrawlerSpider(scrapy.Spider):
    name = 'apartments_crawler'
    allowed_domains = ['www.apartments.com']
    start_urls = ['https://www.apartments.com/fremont-ca/', 'https://www.apartments.com/livermore-ca/']

    def parse(self, response):
        print(f"\n\n{response.url}\n\n")
        link_extractor(link=response.url, pg='', a=[])
        pass
