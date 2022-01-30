import json

import requests
import scrapy
from bs4 import BeautifulSoup
from pydispatch import dispatcher
from scrapy import signals
from scrapy.utils.project import get_project_settings

from src.common import link_extractor, apartments_data_obj

settings = get_project_settings()


class ApartmentsCrawlerSpider(scrapy.Spider):
    name = 'apartments_crawler'
    allowed_domains = ['www.apartments.com']
    start_urls = ['https://www.apartments.com/fremont-ca/', 'https://www.apartments.com/livermore-ca/']

    def __init__(self):
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        self.headers = {'authority': 'www.apartments.com',
                        'cache-control': 'max-age=0',
                        'dnt': '1',
                        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                        'accept-language': 'en-US,en;q=0.9'
                        }
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
        apartments_obj = apartments_data_obj()
        link = url.url
        apartments_obj['link'] = link

        response = requests.get(link, headers=self.headers)
        soup = BeautifulSoup(response.text)

        json_resp = json.loads(soup.find("script", attrs={"type": "application/ld+json"}).text)
        apartments_obj['name'] = json_resp['about']['name'].strip()
        apartments_obj['primary_photo'] = json_resp['about']['image'].strip()
        apartments_obj['description'] = json_resp['about']['description'].replace("\n", "").strip()
        try:
            apartments_obj['property_min_price'] = json_resp['about']['offers']['lowPrice']
            apartments_obj['property_max_price'] = json_resp['about']['offers']['highPrice']
        except Exception as e:
            print(f"Range Error: {e}")
        apartments_obj['phone_number'] = json_resp['mainEntity'][0]['telephone'].strip()
        apartments_obj['locality'] = json_resp['mainEntity'][0]['address']['addressLocality'].strip()
        apartments_obj['region'] = json_resp['mainEntity'][0]['address']['addressRegion'].strip()
        apartments_obj['pin_code'] = int(json_resp['mainEntity'][0]['address']['postalCode'].strip())
        apartments_obj['country'] = json_resp['mainEntity'][0]['address']['addressCountry'].strip()

        apartments_obj['address'] = json_resp['mainEntity'][0]['address']['streetAddress'].strip() + ", " + \
                                    json_resp['mainEntity'][0]['address']['addressLocality'].strip() + ", " + \
                                    json_resp['mainEntity'][0]['address']['addressRegion'].strip() + ", " + \
                                    json_resp['mainEntity'][0]['address']['addressCountry'].strip() + ' - ' + \
                                    json_resp['mainEntity'][0]['address']['postalCode'].strip()
        apartments_obj['latitude'] = float(json_resp['mainEntity'][0]['geo']['latitude'])
        apartments_obj['longitude'] = float(json_resp['mainEntity'][0]['geo']['longitude'])
        try:
            apartments_obj['property_type'] = json_resp['mainEntity'][0]['containsPlace']['@type'].title().strip()
        except Exception as e:
            print(f"Place Error: {e}")
        try:
            apartments_obj['petsAllowed'] = json_resp['mainEntity'][0]['containsPlace']['petsAllowed']
        except Exception as e:
            print(f"Pet Error: {e}")
        # Opening timings
        try:
            for i in json_resp['mainEntity'][0]['openingHoursSpecification']:
                apartments_obj['opening_timings'].extend(
                    [{"day": j, "opens": i['opens'], "closes": i['closes']} for j in i['dayOfWeek']])
        except Exception as e:
            print(f"Opening Hours Error: {e}")
            # print("fetching")
        # print(url)
        # print(json_resp)

        print(f"\n\n{link}: \n{apartments_obj}\n\n")

        yield apartments_obj
        pass
