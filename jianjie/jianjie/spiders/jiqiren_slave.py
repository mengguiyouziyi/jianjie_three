# -*- coding: utf-8 -*-
import scrapy
import time
from urllib.parse import urljoin
from scrapy.selector import Selector
from scrapy.exceptions import CloseSpider
from jianjie.items import JiqirenItem
from jianjie.utils.info import rc


class TouzishijianSpider(scrapy.Spider):
	name = 'jiqiren_slave'

	# custom_settings = {
	# 	'DEFAULT_REQUEST_HEADERS': {
	# 		'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
	# 		'accept-encoding': "gzip, deflate",
	# 		'accept-language': "zh-CN,zh;q=0.8",
	# 		'cache-control': "no-cache",
	# 		# 'connection': "keep-alive",
	# 		# 'cookie': "UM_distinctid=15fc95c2872d78-0fdfee884d9db7-31637e01-13c680-15fc95c28748a8; CNZZDATA3130222=cnzz_eid%3D346745979-1510908079-%26ntime%3D1510924313; Hm_lvt_99d3e8dc9c4fb1796f922e4fc84251b1=1510911782; Hm_lpvt_99d3e8dc9c4fb1796f922e4fc84251b1=1510928806; AJSTAT_ok_pages=9; AJSTAT_ok_times=2; __tins__5221700=%7B%22sid%22%3A1510928732944%2C%22vd%22%3A9%2C%22expires%22%3A1510930606401%7D; __51cke__=; __51laig__=10",
	# 		'host': "www.robot-china.com",
	# 		'upgrade-insecure-requests': "1",
	# 		# 'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
	# 		# 'postman-token': "455d07fb-baa0-faf6-92c9-95ea6a2d771c"
	# 	}
	# }

	def start_requests(self):
		# jiqiren_cats = ['弧焊机器人~http://www.robot-china.com/company/list-4-3.html']
		# for jiqiren_cat in jiqiren_cats:
		x = 0
		while True:
			jiqiren_cat = rc.rpop('jiqiren_cat')
			if not jiqiren_cat:
				# x += 1
				# if x > 5:
					raise CloseSpider('no datas')
				# time.sleep(60)
				# continue
			ll = jiqiren_cat.split('~')
			cat_url = ll[1]
			cat = ll[0]
			yield scrapy.Request(cat_url, callback=self.parse_list, meta={'cat_url': cat_url, 'cat': cat})

	def parse_list(self, response):
		cat_url = response.meta.get('cat_url')
		cat = response.meta.get('cat')
		select = Selector(text=response.text)
		a_tags = select.xpath('//*[@id="item_"]')
		for a_tag in a_tags:
			item = JiqirenItem()
			comp_url = a_tag.xpath('./a/@href').extract_first()
			comp_name = a_tag.xpath('./a/div/b/text()').extract_first()
			zhuying = a_tag.xpath('./a/div/span/text()').extract_first()
			loc = a_tag.xpath('./div[@class="xieceprolitur"]/span/p/text()').extract_first()
			loc = loc.replace('[', '').replace(']', '') if loc else ''
			loc_list = loc.split('/')
			sheng = shi = ''
			if len(loc_list) == 1:
				if loc in ['北京', '上海', '天津', '重庆']:
					sheng = loc
					shi = loc + '市'
				else:
					sheng = loc
			elif len(loc_list) == 2:
				sheng = loc_list[0]
				shi = loc_list[1]
			item['cat_url'] = cat_url
			item['cat'] = cat
			item['comp_url'] = comp_url
			item['comp_name'] = comp_name
			item['zhuying'] = zhuying
			item['loc'] = loc
			item['sheng'] = sheng
			item['shi'] = shi
			yield scrapy.Request(comp_url + 'introduce/', callback=self.parse_detail, meta={'item': item},
			                     dont_filter=True)

	def parse_detail(self, response):
		item = response.meta.get('item')
		if not item:
			return
		select = Selector(text=response.text)
		text = select.xpath('//div[@class="main_body"]//td//text()').extract()
		intro = ''.join([t.strip().replace('\r', '').replace('\t', '').replace('    ', '').replace(' ', '').replace(
			'  ', '').replace('   ', '').replace('██', '').replace('企   业   简   介', '') for t in text if
		                 t]) if text else ''
		item['intro'] = intro
		yield item
