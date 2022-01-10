# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CanadajobsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    company   = scrapy.Field()
    href  = scrapy.Field()
    location  = scrapy.Field()
    salary    = scrapy.Field()
    date = scrapy.Field()
    pass
