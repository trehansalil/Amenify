import scrapy
from pymongo import MongoClient
from scrapy.utils.project import get_project_settings

settings = get_project_settings()
time_choice = [3, 4, 5]


def save_apartments_data_to_db(self, apartments_object):
    mycol = self.apartments_collection
    if mycol.find({"link": apartments_object["link"]}).count() > 0:
        print("Apartmemts Data Already Exists\n")
        for x in mycol.find({"link": apartments_object["link"]}):
            existing = x
            break

        print(existing['created_on'], apartments_object['created_on'])

        mycol.replace_one({"link": apartments_object["link"]}, existing)
        print('--------', existing)
        print("Apartmemts Data Updated\n")
    else:
        print("Inserting Movie into ", mycol)
        mycol.insert_one(apartments_object)
        print("Inserting new apartment data into ", mycol)


class Apartments(scrapy.Spider):
    name = 'apartments'
    allowed_domains = ['apartments.com']
    start_urls = ['https://www.apartments.com']
    # DB_URI = settings.get("MONGODB_URI")
    DB_URI = settings.get("DB_URI")
    database = MongoClient(DB_URI).get_database()
    apartments_collection = database["apartments"]

    def __init__(self):

        print("Initializing Upload in MongoDB")

    def save_apartments_data_to_db(self, apartments_object):

        mycol = self.apartments_collection
        if mycol.find({"link": apartments_object["link"]}).count() > 0:
            print("Apartmemts Data Already Exists\n")
            for x in mycol.find({"link": apartments_object["link"]}):
                existing = x
                break

            print(existing['created_on'], apartments_object['created_on'])

            mycol.replace_one({"link": apartments_object["link"]}, existing)
            print('--------', existing)
            print("Apartmemts Data Updated\n")
        else:
            print("Inserting Movie into ", mycol)
            mycol.insert_one(apartments_object)
            print("Inserting new apartment data into ", mycol)
