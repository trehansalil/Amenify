import scrapy
from pymongo import MongoClient
from scrapy.utils.project import get_project_settings

settings = get_project_settings()
time_choice = [3, 4, 5]


class Apartments(scrapy.Spider):
    name = 'apartments'
    allowed_domains = ['apartments.com']
    start_urls = ['https://www.apartments.com']
    DB_URI = settings.get("DB_URI")
    database = MongoClient(DB_URI).get_database()
    apartments_collection = database["apartments"]

    def __init__(self):

        print("Initializing Upload in MongoDB")

    # Apartments Data Object Constructor
    def apartments_data_obj(self):
        return ({
            "link": None,
            "name": None,
            "primary_image": None,
            "backdrop": [],
            "posters": [],
            "photos": [],
            "images": [],
            "full_description": None,
            "property_min_price": None,
            "property_max_price": None,
            "phone_number": None,
            "address": None,
            'locality': None,
            'region': None,
            'pin_code': None,
            'country': None,
            'type': None,
            'latitude': None,
            'longitude': None,
            'property_type': None,
            'pets_permitted': None,
            "reviews": [],
            'amenities': [],
            'vicinity': [],
            'neighborhood_description': None,
            'parking': [],
            'leasing_options': None,
            "fee_details": [],
            "pets_details": [],
            "nearby_schools": [],
            "management_company": None,
            "property_info": [],
            "created_on": None,
        })

    # Deduplication Logic for urls
    def check_url(self, link):
        if self.apartments_collection.count_documents({"link": link}) > 0:
            return True

    def save_apartments_data_to_db(self, apartments_object):
        mycol = self.apartments_collection
        # print(mycol.find({}))
        # if mycol.find({}).count() == 0:
        #     print("Inserting new apartment data into ", mycol)
        #     mycol.insert_one(apartments_object)
        #     print("Inserted new apartment data into ", mycol)
        try:
            if mycol.count_documents({"link": apartments_object["link"]}) > 0:
                print("Apartmemts Data Already Exists\n")
                for x in mycol.find({"link": apartments_object["link"]}):
                    existing = x
                    break
                # if existing['link'] == apartments_object['link']:
                #     continue
                print(existing['created_on'], apartments_object['created_on'])

                mycol.replace_one({"link": apartments_object["link"]}, existing)
                print('--------', existing)
                print("Apartmemts Data Updated\n")
            else:
                print("Inserting new apartment data into ", mycol)
                mycol.insert_one(apartments_object)
                print("Inserted new apartment data into ", mycol)
        except Exception as e:
            print(f"Insert Error: {e}")
            print("Inserting new apartment data into ", mycol)
            mycol.insert_one(apartments_object)
            print("Inserted new apartment data into ", mycol)
