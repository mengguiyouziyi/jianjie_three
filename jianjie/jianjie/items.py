# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Huangye88AllItem(scrapy.Item):
	comp_url = scrapy.Field()
	comp_name = scrapy.Field()
	intro = scrapy.Field()
	city = scrapy.Field()


class Huangye88KunmingItem(scrapy.Item):
	comp_url = scrapy.Field()
	comp_name = scrapy.Field()
	intro = scrapy.Field()


class Huangye88LiuzhouItem(scrapy.Item):
	comp_url = scrapy.Field()
	comp_name = scrapy.Field()
	intro = scrapy.Field()


class Huangye88AotuItem(scrapy.Item):
	comp_url = scrapy.Field()
	comp_name = scrapy.Field()
	posi = scrapy.Field()
	shengshi = scrapy.Field()
	# shi = scrapy.Field()
	# xian = scrapy.Field()
	intro = scrapy.Field()
	cat = scrapy.Field()


class ShunqiAllItem(scrapy.Item):
	comp_url = scrapy.Field()
	comp_name = scrapy.Field()
	intro = scrapy.Field()
	city = scrapy.Field()


class ShunqiLiuzhouItem(scrapy.Item):
	comp_url = scrapy.Field()
	comp_name = scrapy.Field()
	intro = scrapy.Field()


class ShunqiKunmingItem(scrapy.Item):
	comp_url = scrapy.Field()
	comp_name = scrapy.Field()
	intro = scrapy.Field()


class MinglujiLiuzhouItem(scrapy.Item):
	comp_url = scrapy.Field()
	comp_name = scrapy.Field()
	intro = scrapy.Field()


class MinglujiKunmingItem(scrapy.Item):
	comp_url = scrapy.Field()
	comp_name = scrapy.Field()
	intro = scrapy.Field()


class WuyouAllItem(scrapy.Item):
	comp_name = scrapy.Field()
	comp_url = scrapy.Field()
	intro = scrapy.Field()
	area = scrapy.Field()


class huang114AllItem(scrapy.Item):
	comp_name = scrapy.Field()
	comp_url = scrapy.Field()
	link_man = scrapy.Field()
	tel = scrapy.Field()
	email = scrapy.Field()
	addr = scrapy.Field()
	intro = scrapy.Field()


class ZhizaoAllItem(scrapy.Item):
	comp_url = scrapy.Field()
	comp_name = scrapy.Field()
	addr = scrapy.Field()
	intro = scrapy.Field()


class Ca800Item(scrapy.Item):
	comp_url = scrapy.Field()
	comp_name = scrapy.Field()
	cat_url = scrapy.Field()
	cat = scrapy.Field()
	loc = scrapy.Field()
	intro = scrapy.Field()
