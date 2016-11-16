from scrapy.item import Item, Field

class ApartmentItem(Item):
    cl_id       = Field()
    title       = Field()
    url         = Field()
    price       = Field()
    latitude    = Field()
    longitude   = Field()
    where       = Field()
    datetime    = Field()

class CarItem(Item):
    cl_id       = Field()
    title       = Field()
    url         = Field()
    price       = Field()
    where       = Field()
    datetime    = Field()
