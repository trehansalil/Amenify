import scrapy
from pydispatch import dispatcher
from scrapy import signals
from scrapy.utils.project import get_project_settings

from src.common import link_extractor

settings = get_project_settings()


class ApartmentsCrawlerSpider(scrapy.Spider):
    name = 'apartments_crawler'
    allowed_domains = ['www.apartments.com']
    start_urls = ['https://www.apartments.com/fremont-ca/', 'https://www.apartments.com/livermore-ca/']

    def __init__(self):
        dispatcher.connect(self.spider_opened, signals.spider_opened)

        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_opened(self, spider):

        print("opening Spider : {}".format(str(spider)))

    def spider_closed(self, spider):
        # close db connection
        print("Closing Spider")

    def parse(self, response):
        print(f"\n\n{response.url}\n\n")
        url_list = link_extractor(link=response.url, pg='', a=[])
        for url in url_list:
            yield scrapy.Request(url=url, callback=self.parse_apartments)
        pass

    def parse_apartments(self, url):
        print(f"\n\n{url}\n\n")
        pass
