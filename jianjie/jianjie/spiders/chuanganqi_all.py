# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin
from scrapy.selector import Selector
from jianjie.items import ChuanItem


class TouzishijianSpider(scrapy.Spider):
	name = 'chuanganqi_all'
	custom_settings = {
		'DEFAULT_REQUEST_HEADERS': {
			'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
			'accept-encoding': "gzip, deflate",
			'accept-language': "zh-CN,zh;q=0.8",
			'cache-control': "no-cache",
			'connection': "keep-alive",
			# 'cookie': "Hm_lvt_4d22079a74c0c1865d034963d557313f=1510911403; Hm_lpvt_4d22079a74c0c1865d034963d557313f=1510934801; Hm_lvt_51c1065086bf6fe4d8f2bcbb06462000=1510911403; Hm_lpvt_51c1065086bf6fe4d8f2bcbb06462000=1510934801",
			'host': "www.chinasensor.cn",
			'if-modified-since': "Thu, 09 Nov 2017 01:27:45 GMT",
			'referer': "http://www.chinasensor.cn/company/chuanganqi/company_list_1.html",
			'upgrade-insecure-requests': "1",
			# 'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
			'postman-token': "7777e054-b87e-2f33-0e51-6eeb797da05d"
		}
	}

	def start_requests(self):
		start_url = "http://www.chinasensor.cn/company/chuanganqi/"
		yield scrapy.Request(start_url)

	def parse(self, response):
		select = Selector(text=response.text)
		li_tags = select.xpath('//div[@class="category"]/div//tr/td/a')
		for li_tag in li_tags:
			cat_url = li_tag.xpath('./@href').extract_first()
			cat_url = urljoin(response.url, cat_url)
			cat = li_tag.xpath('./text()').extract_first()
			yield scrapy.Request(cat_url, callback=self.parse_list, meta={'cat_url': cat_url, 'cat': cat})

	def parse_list(self, response):
		cat_url = response.meta.get('cat_url')
		cat = response.meta.get('cat')
		select = Selector(text=response.text)
		a_tags = select.xpath('//div[@class="list"]/tr[@align="center"]')

		for a_tag in a_tags:
			li_tag = a_tag.xpath('./td[@align="left"]/ul/li')
			li_tag.xpath('/')




			item = ChuanItem()
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
			yield scrapy.Request(comp_url + 'introduce/', callback=self.parse_detail, meta={'item': item})
		p_next = select.xpath('//a[@class="next"]/@href').extract_first()
		if not p_next:
			return
		yield scrapy.Request(p_next, callback=self.parse_list, meta={'cat_url': cat_url, 'cat': cat})

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
