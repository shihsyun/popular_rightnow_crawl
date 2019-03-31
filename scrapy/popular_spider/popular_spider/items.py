# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class PopularSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    shop_name = scrapy.Field()
    shop_url = scrapy.Field()
    bestseller = scrapy.Field()
    image_url = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    appeardate = scrapy.Field()
