# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Roster(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    date = scrapy.Field()
    level = scrapy.Field()

class Player(scrapy.Item):
    name = scrapy.Field()
    club = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    position = scrapy.Field()
    level = scrapy.Field()
    date = scrapy.Field()

