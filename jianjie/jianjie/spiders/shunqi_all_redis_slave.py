# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.selector import Selector
from scrapy.exceptions import CloseSpider
from jianjie.items import ShunqiAllItem
from jianjie.utils.bloomfilter import rc


class TouzishijianSpider(scrapy.Spider):
	name = 'shunqi_all_redis_slave'
	custom_settings = {
		'DEFAULT_REQUEST_HEADERS': {
			'upgrade-insecure-requests': "1",
			'x-devtools-emulate-network-conditions-client-id': "f0a03c13-8b72-438f-ad7d-d7b080ebe859",
			# 'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
			'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
			'accept-encoding': "gzip, deflate",
			'accept-language': "zh-CN,zh;q=0.8",
			# 'cookie': "Hm_lvt_819e30d55b0d1cf6f2c4563aa3c36208=1508817163; Hm_lpvt_819e30d55b0d1cf6f2c4563aa3c36208=1508831973",
			'cache-control': "no-cache",
			'postman-token': "113cbae1-205e-e6e2-1b90-ccef268bf099"
		}
	}

	def start_requests(self):
		x = 0
		while True:
			com_id_name = rc.spop('shunqi_all_detail')

			if not com_id_name:
				x += 1
				if x > 5:
					raise CloseSpider('no datas')
				time.sleep(60)
				continue

			lis = com_id_name.split('//')
			city = lis[0]
			comp_url = 'http://' + lis[1]
			item = ShunqiAllItem()
			item['city'] = city
			yield scrapy.Request(comp_url, meta={'item': item})

	def parse_detail(self, response):
		item = response.meta.get('item')
		sel = Selector(text=response.text)
		comp_name = sel.xpath('//div[@class="navleft"]/a[last()]/text()').extract_first()
		intros = sel.xpath('//div[@class="boxcontent text"]//text()').extract()
		intro = ''.join(intros) if intros else ''
		intro = intro.strip()
		item['comp_url'] = response.url
		item['comp_name'] = comp_name
		item['intro'] = intro
		# item['city'] = re.search(r'http://www\.11467\.com/(.*)/co/\d+.htm', response.url).group(1)

		yield item
