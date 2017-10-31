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
		# p_num_str = sel.xpath('//span[@class="text"]/text()').extract_first()
		# p_num = re.search(r'\d+', p_num_str).group()
		# http://www.huangye88.com/search.html?kw=%E5%87%B9%E5%9C%9F&type=company&page=205/
		# http://www.huangye88.com/search.html?kw=%E5%87%B9%E5%9C%9F&type=company&
		p_num_url = sel.xpath('//a[@class="pag nextpage"]/@href').extract_first()
		p_num_url = urljoin(response.url, p_num_url)
		if not p_num_url:
			return
		yield scrapy.Request(p_num_url, meta={'cat': cat})



	# def parse_city(self, response):
	# 	item = response.meta.get('item')
	# 	sel = Selector(text=response.text)
	# 	cat_tags = sel.xpath('//ul[@class="clearfix"]/li/a')
	# 	for cat_tag in cat_tags:
	# 		cat_url = cat_tag.xpath('./@href').extract_first()
	# 		cat = re.search(r'com/.*/([-\w+]+)/$', cat_url).groups()[0]
	# 		# cat_name = cat_tag.xpath('./text()').extract_first()
	# 		yield scrapy.Request(cat_url, callback=self.parse_list, meta={'cat': cat, 'item': item})

	# def parse_list(self, response):
	# 	item = response.meta.get('item')
	# 	sel = Selector(text=response.text)
	# 	comp_urls = sel.xpath('//*[@id="jubao"]/dl/dt/h4/a/@href|//ul[@class="news"]/li/a/@href').extract()
	# 	for comp_url in comp_urls:
	# 		comp_detail_url = comp_url + 'company_detail.html'
	# 		yield scrapy.Request(comp_detail_url, callback=self.parse_detail, meta={'item': item})
	# 	if 'm.huangye88.com/b2b/' in response.url:
	# 		return
	# 	pn_str = sel.xpath('//div[@class="tit tit2"]/span/em/text()').extract_first()
	# 	pn = ceil(int(pn_str) / 20)
	# 	pn_now_re = re.search(r'/pn(\d+)/$', response.url)
	# 	pn_now = int(pn_now_re.groups()[0]) if pn_now_re else 1
	# 	if pn_now >= pn:
	# 		return
	# 	cat = response.meta.get('cat', '')
	# 	yield scrapy.Request(self.burl.format(cat, (pn_now + 1)), callback=self.parse_list,
	# 	                     meta={'cat': cat, 'item': item})

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
