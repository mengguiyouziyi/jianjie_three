# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Huangye88KunmingItem(scrapy.Item):
	comp_url = scrapy.Field()
	comp_name = scrapy.Field()
	intro = scrapy.Field()


class Huangye88LiuzhouItem(scrapy.Item):
	comp_url = scrapy.Field()
	comp_name = scrapy.Field()
	intro = scrapy.Field()


class ShunqiLiuzhouItem(scrapy.Item):
	comp_url = scrapy.Field()
	comp_name = scrapy.Field()
	intro = scrapy.Field()


class ShunqiKunmingItem(scrapy.Item):
	comp_url = scrapy.Field()
	comp_name = scrapy.Field()
	intro = scrapy.Field()