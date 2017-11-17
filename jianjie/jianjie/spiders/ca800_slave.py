# -*- coding: utf-8 -*-
import scrapy
import re
import time
from urllib.parse import urljoin
from scrapy.selector import Selector
from jianjie.items import Ca800Item
from jianjie.utils.info import rc
from scrapy.exceptions import CloseSpider


class TouzishijianSpider(scrapy.Spider):
	name = 'ca800_slave'

	# custom_settings = {
	# 	'DEFAULT_REQUEST_HEADERS': {
	# 		'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
	# 		'accept-encoding': "gzip, deflate",
	# 		'accept-language': "zh-CN,zh;q=0.8",
	# 		'cache-control': "no-cache",
	# 		# 'connection': "keep-alive",
	# 		# 'cookie': "ASP.NET_SessionId=kh5iqkvjtb4vjthzf40t54x1; cookiesmark=2017111717345000003; Hm_lvt_57a0c48ef04a2d3a7e7dec8e459b2bb4=1510911322; Hm_lpvt_57a0c48ef04a2d3a7e7dec8e459b2bb4=1510911380; sid=2017111717351400003; vid=2017111717351400004; _ga=GA1.2.332251248.1510911440; _gid=GA1.2.926593169.1510911440",
	# 		'host': "www.ca800.com",
	# 		'upgrade-insecure-requests': "1",
	# 		# 'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
	# 		# 'postman-token': "05eca74f-a731-dd48-9e85-fba7ae401bc6"
	# 	}
	# }

	def start_requests(self):
		x = 0
		while True:
			jiqiren_cat = rc.rpop('ca800_all')
			if not jiqiren_cat:
				x += 1
				if x > 5:
					raise CloseSpider('no datas')
				time.sleep(60)
				continue
			yield scrapy.Request(jiqiren_cat)

	def parse(self, response):
		select = Selector(text=response.text)
		li_tags = select.xpath('//div[@class="factlist"]/ul/li')
		# print(len(li_tags))
		for li_tag in li_tags:
			item = Ca800Item()
			a_tag = li_tag.xpath('./div[@class="facrlist_title"]/a')
			comp_url = a_tag.xpath('./@href').extract_first()
			# print(comp_url)
			comp_url = urljoin(response.url, comp_url) if comp_url else ''
			comp_url = comp_url.replace('index.html', 'intro.html')
			if not comp_url:
				return
			comp_name = a_tag.xpath('./text()').extract()
			comp_name = ''.join(
				[c.strip().replace('\r', '').replace('\t', '') for c in comp_name if c]) if comp_name else ''

			cat_tag = li_tag.xpath('./div[@class="facrlist_guild"]')
			cat_a_tag = cat_tag.xpath('./a')
			cat_url = cat_a_tag.xpath('./@href').extract_first()
			cat_url = urljoin(response.url, cat_url) if cat_url else ''
			cat = cat_a_tag.xpath('./text()').extract_first()

			loc_str = cat_tag.xpath('./text()').extract()
			loc_str = ''.join([s.strip().replace('\r', '').replace('\t', '') for s in loc_str if s]) if loc_str else ''
			loc = re.search(r'所在地：(.*)', loc_str).group(1)
			lia = re.search(r'(.*)-(.*)', loc)
			lia = lia.groups() if lia else []
			sheng = lia[0] if len(lia) > 1 else ''
			shi = lia[1] if len(lia) > 1 else lia[0]

			intro = li_tag.xpath('./p/text()').extract_first()

			item['comp_url'] = comp_url
			item['comp_name'] = comp_name
			item['cat_url'] = cat_url
			item['cat'] = cat
			item['loc'] = loc
			item['sheng'] = sheng
			item['shi'] = shi
			item['intro'] = intro

			yield scrapy.Request(comp_url, callback=self.parse_detail, meta={'item': item})

	def parse_detail(self, response):
		item = response.meta.get('item', '')
		if not item:
			return
		if 'intro' not in response.url:
			# print('no intro  ', response.url)
			yield item
			return
		select = Selector(text=response.text)
		text = select.xpath('//div[@class="main-box"]/div[@class="detail"]//text()').extract()
		intro = ''.join([t.strip().replace('\r', '').replace('\t', '').replace('    ', '').replace(' ', '').replace(
			'  ', '').replace('   ', '').replace('██', '').replace('企   业   简   介', '') for t in text if
		                 t]) if text else ''
		item['intro'] = intro
		yield item
