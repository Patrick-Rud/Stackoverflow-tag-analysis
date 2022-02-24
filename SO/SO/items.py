# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    qid = scrapy.Field()
    qvotes = scrapy.Field()
    qanswers = scrapy.Field()
    qviews = scrapy.Field()
    qasktime = scrapy.Field()
    qactivetime = scrapy.Field()
    avotesum = scrapy.Field()
    responsetime = scrapy.Field()

