import json
import random
import ssl
import time
import urllib.request

import requests
import scrapy
from PIL import Image
from bs4 import BeautifulSoup
from pydispatch import dispatcher
from scrapy import signals
from scrapy.utils.project import get_project_settings

from src.common import link_extractor, image_extractor, education_data_fetcher
from src.review import reviews_extractor
from datetime import datetime
from src.apartment import Apartments

settings = get_project_settings()
sleep_times = [3, 4, 5]
context = ssl._create_unverified_context()

apartments = Apartments()


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
        for enum, url in enumerate(url_list):
            # if enum > 20:
            #     break
            if apartments.check_url(link=url):
                print(f"\n\n Enum {enum} Skipping this url: {url}\n\n")
                continue
            time.sleep(random.choice(sleep_times))
            print(f"Enum {enum} : {url}")

            yield scrapy.Request(url=url, callback=self.parse_apartments)
        pass

    def parse_apartments(self, url):
        apartments_obj = apartments.apartments_data_obj()
        link = url.url

        apartments_obj['link'] = link

        response = requests.get(link, headers=self.headers)
        soup = BeautifulSoup(response.text)

        json_resp = json.loads(soup.find("script", attrs={"type": "application/ld+json"}).text)
        apartments_obj['name'] = json_resp['about']['name'].strip()
        apartments_obj['primary_image'] = json_resp['about']['image'].strip()
        apartments_obj['full_description'] = json_resp['about']['description'].replace("\n", "").strip()
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
            apartments_obj['pets_permitted'] = json_resp['mainEntity'][0]['containsPlace']['petsAllowed']
        except Exception as e:
            print(f"Pet Error: {e}")
            # print("fetching")
        # print(url)
        # print(json_resp)

        # apartments_obj['reviews'] = reviews_extractor(link=link)
        # apartments_obj['images'] = image_extractor(link=link)

        for img_url in apartments_obj['images']:
            req = urllib.request.urlopen(img_url, context=context)
            img = Image.open(req)
            if img.size[0] > img.size[1]:
                apartments_obj['backdrops'].append(img_url)
            elif img.size[0] < img.size[1]:
                apartments_obj['posters'].append(img_url)
            else:
                apartments_obj['photos'].append(img_url)

        # Amenities data
        for amenities in soup.find_all("li", attrs={"class": "specInfo"})[1:]:
            apartments_obj["amenities"].append(amenities.text.strip())

        # fetching nearby areas
        dict_value = {}
        for contents in soup.select(".transportationDetail"):
            row = []
            for child in contents.find("table").children:
                for td in child:
                    try:
                        alpha = [i for i in td.text.split('\n') if i and len(i) != 0]

                        if alpha not in row and len(alpha) != 0:
                            row.append(alpha)
                    except:
                        continue
            dict_value.update({row[0][0]: {i[0]: i[1:] for i in row[1:]}})

        apartments_obj["vicinity"].append(dict_value)

        # neighborhood description
        desc = []
        [desc.extend(i.find_all("p")) for i in soup.find_all("div", attrs={"class": "overView"})]
        apartments_obj["neighborhood_description"] = [i.get_text().strip() for i in desc if i.get_text().strip()]

        # Parking details, Pet details, Leasing details
        data_fetch = {i: i.find("h4").get_text() if i.find("h4") is not None else None for i in
                      soup.select(".component-frame")}
        for i in data_fetch.values():
            if "Other Fees" == str(i).strip():
                print(i)

        value_fetch = [i for i in data_fetch.values()]
        index_fetch = [i for i in data_fetch.keys()]
        # result_fetch = {value_fetch[i]: index_fetch[i] for i in range(len(index_fetch))}
        try:
            keys = [i.get_text() for i in index_fetch[value_fetch.index("Parking")].select(".column")]
            values = [i.get_text() for i in index_fetch[value_fetch.index("Parking")].select(".subTitle")]
            result_fetch = {keys[i]: values[i] for i in range(len(keys))}
            apartments_obj['parking'].append(result_fetch)
        except Exception as e:
            print(f"Parking Error: {e}")

        # Leasing details
        try:
            lease_value = [i.get_text() for i in index_fetch[value_fetch.index("Lease Options")].select(".column")]
            apartments_obj["leasing_options"] = lease_value
        except Exception as e:
            print(f"Lease Option Error: {e}")

        # Fees details
        try:
            fee_keys = [i.get_text() for i in index_fetch[value_fetch.index("Other Fees")].select(".column")]
            fee_values = [i.get_text() for i in index_fetch[value_fetch.index("Other Fees")].select(".column-right")]
            fees_details = {fee_keys[i]: fee_values[i] for i in range(len(fee_keys))}
            apartments_obj["fee_details"].append(fees_details)
        except Exception as e:
            print(f"Other Fees Error: {e}")

        # Pet Details
        try:
            pet_keys = [i.get_text() for i in index_fetch[value_fetch.index("Dogs Allowed")].select(".column")]
            pet_values = [i.get_text() for i in index_fetch[value_fetch.index("Dogs Allowed")].select(".column-right")]
            pet_details = {pet_keys[i]: pet_values[i] for i in range(len(pet_keys))}
            apartments_obj["pets_details"].append(pet_details)
        except Exception as e:
            print(f"Pet Details Error: {e}")

        # fetching nearby school details
        try:
            for j in ["Public", "Private"]:
                apartments_obj["nearby_schools"].append(education_data_fetcher(soup=soup, typ=j))
        except Exception as e:
            print(f"Education Error: {e}")

        # management company
        apartments_obj["management_company"] = soup.select_one(".pmcLogo")['src'].split('/')[-1].split('.')[0].replace(
            '-logo', '').replace('-', ' ').title()

        # Fetching the property stories and floor details
        try:
            stories_fetch = [i.get_text() for i in
                             index_fetch[value_fetch.index("Property Information")].select(".column")]
            property_data = [i for i in stories_fetch if i.count("units") or i.count("stories")]
            apartments_obj["property_info"] = property_data
        except Exception as e:
            print(f"Other stories/units Error: {e}")

        print(f"\n\n{link}: \n{apartments_obj}\n\n")
        apartments_obj['created_on'] = datetime.now()

        apartments.save_apartments_data_to_db(apartments_object=apartments_obj)

        yield apartments_obj
        pass
