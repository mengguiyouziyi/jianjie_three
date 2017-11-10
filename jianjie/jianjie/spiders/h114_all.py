# -*- coding: utf-8 -*-
import os
import sys
from os.path import dirname

ffather_path = dirname(dirname(dirname(os.path.abspath(dirname(__file__)))))
father_path = dirname(dirname(os.path.abspath(dirname(__file__))))
base_path = dirname(dirname(os.path.abspath(dirname(__file__))))
path = dirname(os.path.abspath(dirname(__file__)))
sys.path.append(path)
sys.path.append(base_path)
sys.path.append(father_path)
sys.path.append(ffather_path)
# import scrapy
# import time
# from jianjie.utils.bloomfilter import rc
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
# from scrapy.exceptions import CloseSpider
from jianjie.items import huang114AllItem


class TouzishijianSpider(CrawlSpider):
	name = 'huang114_all'
	allowed_domains = ['114chn.com']
	start_urls = ['http://www.114chn.com/']
	custom_settings = {
		'DEFAULT_REQUEST_HEADERS': {
			'upgrade-insecure-requests': "1",
			# 'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
			'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
			'referer': "http://search.114chn.com/searchresult.aspx?type=1&areaid=31&pattern=2&page=100",
			'accept-encoding': "gzip, deflate",
			'accept-language': "zh-CN,zh;q=0.8",
			# 'cookie': "bdshare_firstime=1509612560767; UM_distinctid=15f7bed65c32e0-01af79ead3a85f-31637e01-13c680-15f7bed65c4735; Hm_lvt_40b8d9bb56b7b9b3fee170b6b9b4bc8e=1509612561; Hm_lpvt_40b8d9bb56b7b9b3fee170b6b9b4bc8e=1509613182; CNZZDATA30067493=cnzz_eid%3D1102648662-1510104203-http%253A%252F%252Fsearch.114chn.com%252F%26ntime%3D1510104203",
			'cache-control': "no-cache",
			'postman-token': "b710e80f-5152-1b73-ed8c-b5342bd0c5a9"
		}
	}

	# def start_requests(self):
	# 	burl = 'http://search.114chn.com/searchresult.aspx?type=1&key={k}&pattern=2&page=1'
	# 	x = 0
	# 	while True:
	# 		comp_name = rc.spop('zhuce_names')
	# 		if not comp_name:
	# 			x += 1
	# 			if x > 5:
	# 				raise CloseSpider('no datas')
	# 			time.sleep(60)
	# 			continue
	# 		url = burl.format(k=comp_name)
	# 		yield scrapy.Request(url, meta={'dont_redirect': True})

		# start_url = "http://search.114chn.com/searchresult.aspx?type=1&areaid={area}&pattern=2&page=100"
		# for i in range(100):
		# 	yield scrapy.Request(start_url.format(area=str(i)), dont_filter=True)

	rules = (
		# Rule(LinkExtractor(allow=('searchresult',))),
		Rule(LinkExtractor(allow=('.*',))),
		Rule(
			LinkExtractor(
				allow=(
					'TradeDetail\.aspx',
					'Free\.aspx'
				)
			),
			callback='parse_item'
		),
	)

	def parse_item(self, response):
		item = huang114AllItem()
		if '很抱歉！页面在您访问时发生了错误' in response.text or '对不起 ！' in response.text:
			return
		select = Selector(text=response.text)
		if 'freeindex' in response.url:
			comp_name = select.xpath('//*[@id="lblCompanyName"]//text()').extract_first()
			link_man = select.xpath('//*[@id="lblLinkMan"]//text()').extract_first()
			tel = select.xpath('//*[@id="lblTel"]/text()').extract_first()
			email = select.xpath('//*[@id="lblEmail"]/text()').extract_first()
			addr = select.xpath('//*[@id="lblAddress"]/text()').extract_first()
			t = select.xpath('//*[@id="lblContent"]//text()').extract()
			intro = ''.join(t) if t else ''
		else:
			comp_name = select.xpath('//div[@class="zitifree"]/text()').extract_first()
			link_man = select.xpath('//*[@class="lblLinkMan"]//text()').extract_first()
			tel = select.xpath('//*[@class="lbltel"]/text()').extract_first()
			email = select.xpath('//*[@class="lblemail"]/text()').extract_first()
			addr = select.xpath('//*[@class="lblweb"]/text()').extract_first()
			t = select.xpath('//div[@class="xinxi"]//text()').extract()
			intro = ''.join(t) if t else ''
		item['comp_url'] = response.url
		item['comp_name'] = comp_name.strip() if comp_name else ''
		item['link_man'] = link_man
		item['tel'] = tel
		item['email'] = email
		item['addr'] = addr
		item['intro'] = intro
		yield item
