# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.selector import Selector
from math import ceil
from jianjie.items import Huangye88KunmingItem


class TouzishijianSpider(scrapy.Spider):
	name = 'huangye88_kunming'
	burl = 'http://b2b.huangye88.com/kunming/{}/pn{}/'
	custom_settings = {
		'DEFAULT_REQUEST_HEADERS': {
			'x-devtools-emulate-network-conditions-client-id': "82dfd7c8-61b5-4d6e-be6b-737478ed94c1",
			'upgrade-insecure-requests': "1",
			# 'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
			'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
			'referer': "http://b2b.huangye88.com/yunnan/",
			'accept-encoding': "gzip, deflate",
			'accept-language': "zh-CN,zh;q=0.8",
			# 'cookie': "PHPSESSID=4040d366a1b443148ac52884266bed3659eeb167d63461.93983296; _ga=GA1.2.1756847603.1508815209; _gid=GA1.2.343721429.1508815209; Hm_lvt_c8184fd80a083199b0e82cc431ab6740=1508815209; Hm_lpvt_c8184fd80a083199b0e82cc431ab6740=1508815666",
			'cache-control': "no-cache",
			'postman-token': "41f85de8-6890-17d4-f427-410383245168"
		}
	}

	def start_requests(self):
		start_url = "http://b2b.huangye88.com/kunming/"
		yield scrapy.Request(start_url)

	def parse(self, response):
		sel = Selector(text=response.text)
		cat_tags = sel.xpath('//ul[@class="clearfix"]/li/a')
		for cat_tag in cat_tags:
			cat_url = cat_tag.xpath('./@href').extract_first()
			cat = re.search(r'com/kunming/([-\w+]+)/$', cat_url).groups()[0]
			# cat_name = cat_tag.xpath('./text()').extract_first()
			yield scrapy.Request(cat_url, callback=self.parse_list, meta={'cat': cat})

	def parse_list(self, response):
		print(response.url)
		sel = Selector(text=response.text)
		comp_urls = sel.xpath('//*[@id="jubao"]/dl/dt/h4/a/@href|//ul[@class="news"]/li/a/@href').extract()
		for comp_url in comp_urls:
			comp_detail_url = comp_url + 'company_detail.html'
			yield scrapy.Request(comp_detail_url, callback=self.parse_detail)
		if 'm.huangye88.com/b2b/' in response.url:
			return
		pn_str = sel.xpath('//div[@class="tit tit2"]/span/em/text()').extract_first()
		pn = ceil(int(pn_str) / 20)
		pn_now_re = re.search(r'/pn(\d+)/$', response.url)
		pn_now = int(pn_now_re.groups()[0]) if pn_now_re else 1
		if pn_now >= pn:
			return
		cat = response.meta.get('cat', '')
		yield scrapy.Request(self.burl.format(cat, (pn_now + 1)), callback=self.parse_list, meta={'cat': cat})

	def parse_detail(self, response):
		item = Huangye88KunmingItem()
		sel = Selector(text=response.text)
		comp_name = sel.xpath('//p[@class="com-name"]/text()|//h1[@class="banner-text"]/a/text()').extract_first()
		intros = sel.xpath('//p[@class="txt"]/text()|//div[@class="com-intro"]/p/text()').extract()
		intro = ''.join(intros) if intros else ''
		item['comp_url'] = response.url
		item['comp_name'] = comp_name
		item['intro'] = intro

		yield item
