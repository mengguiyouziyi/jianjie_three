# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from jianjie.items import ShunqiLiuzhouItem


class TouzishijianSpider(scrapy.Spider):
	name = 'shunqi_liuzhou'
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
		start_url = "http://www.11467.com/liuzhou/"
		yield scrapy.Request(start_url)

	def parse(self, response):
		sel = Selector(text=response.text)
		cat_tags = sel.xpath('//div[@class="boxcontent"]/ul[@class="listtxt"]/li/dl/dt/a')
		for cat_tag in cat_tags:
			cat_url = cat_tag.xpath('./@href').extract_first()
			yield scrapy.Request(cat_url, callback=self.parse_list)

	def parse_list(self, response):
		print(response.url)
		sel = Selector(text=response.text)
		comp_urls = sel.xpath('//div[@class="f_l"]/h4/a/@href').extract()
		for comp_url in comp_urls:
			yield scrapy.Request('http:'+comp_url, callback=self.parse_detail)

		pn_next = sel.xpath('//div[@class="pages"]/a[text()="下一页"]/@href').extract_first()
		pn_last = sel.xpath('//div[@class="pages"]/a[text()="尾页"]/@href').extract_first()
		pn_ne = pn_next if pn_next else pn_last
		pn_nex = pn_ne if pn_ne else ''
		if not pn_nex:
			return
		yield scrapy.Request('http:'+pn_ne, callback=self.parse_list)

	def parse_detail(self, response):
		item = ShunqiLiuzhouItem()
		sel = Selector(text=response.text)
		comp_name = sel.xpath('//div[@class="navleft"]/a[last()]/text()').extract_first()
		intros = sel.xpath('//div[@class="boxcontent text"]//text()').extract()
		intro = ''.join(intros) if intros else ''
		intro = intro.strip()
		item['comp_url'] = response.url
		item['comp_name'] = comp_name
		item['intro'] = intro

		yield item
