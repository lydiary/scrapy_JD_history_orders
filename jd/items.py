# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    product_name = scrapy.Field()
    receive_user = scrapy.Field()
    number = scrapy.Field()
    price = scrapy.Field()
    status = scrapy.Field()
    dealtime = scrapy.Field()
