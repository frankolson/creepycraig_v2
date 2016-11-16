import pymongo
from scrapy.conf import settings
from creepycraig_v2.items import ApartmentItem, CarItem


class ApartmentPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_APA_COLLECTION']] # use the person collection

    def process_item(self, item, spider):
        if not isinstance(item, ApartmentItem):
            return item # return the item to let another pipeline to handle it
        self.collection.insert(dict(item))

class CarPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_CTO_COLLECTION']] # use the book collection

    def process_item(self, item, spider):
        if not isinstance(item, CarItem):
            return item # return the item to let another pipeline to handle it
        self.collection.update({'cl_id': item['cl_id']}, dict(item), upsert=True)
        self.collection.insert(dict(item))
