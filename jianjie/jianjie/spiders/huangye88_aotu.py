# -*- coding: utf-8 -*-
import scrapy
import re
from urllib.parse import urljoin
from scrapy.selector import Selector
from math import ceil
from jianjie.items import Huangye88AotuItem


class TouzishijianSpider(scrapy.Spider):
	name = 'huangye88_aotu'
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
		sear = ['凹土', '干燥剂', '脱色剂', '分子筛', '催化剂']
		for s in sear:
			start_url = "http://www.huangye88.com/search.html?kw={}&type=company".format(s)
			# start_url = "http://www.huangye88.com/search.html?kw=%E5%87%B9%E5%9C%9F&type=company"
			yield scrapy.Request(start_url, meta={'cat': s})

	def parse(self, response):
		cat = response.meta.get('cat')
		sel = Selector(text=response.text)
		a_tags = sel.xpath('//p[@class="p-title"]/a')
		for a in a_tags:
			item = Huangye88AotuItem()
			item['cat'] = cat
			comp_name = a.xpath('./text()').extract_first()
			url = a.xpath('./@href').extract_first()
			item['comp_name'] = comp_name
			yield scrapy.Request(url + 'company_detail.html', callback=self.parse_detail, meta={'item': item})
		p_num_url = sel.xpath('//a[@class="pag nextpage"]/@href').extract_first()
		p_num_url = urljoin(response.url, p_num_url)
		if not p_num_url:
			return
		yield scrapy.Request(p_num_url, meta={'cat': cat})

	def parse_detail(self, response):
		item = response.meta.get('item')
		sel = Selector(text=response.text)
		# comp_name = sel.xpath('//p[@class="com-name"]/text()|//h1[@class="banner-text"]/a/text()').extract_first()
		intros = sel.xpath('//p[@class="txt"]/text()|//div[@class="com-intro"]/p/text()').extract()
		intro = ''.join(intros) if intros else ''
		item['comp_url'] = response.url
		# item['comp_name'] = comp_name
		item['intro'] = intro.strip()
		td_tags = sel.xpath('//div[@class="r-content"]//td')
		posi = ''
		for td in td_tags:
			span = td.xpath('./span/text()').extract_first()
			if '公司地址' != span:
				continue
			posi = td.xpath('./text()').extract_first()
		item['posi'] = posi

		ul_tags = sel.xpath('//ul[@class="con-txt"]/li|//ul[@class="pro-list"]/li')
		shengshi = ''
		for ul in ul_tags:
			label = ul.xpath('./label/text()').extract_first()
			if '所在地' not in label:
				continue
			shengshi = ul.xpath('./text()').extract_first()
		item['shengshi'] = shengshi

		yield item
