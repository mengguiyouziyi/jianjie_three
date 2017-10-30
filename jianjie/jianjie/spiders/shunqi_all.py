# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin
from scrapy.selector import Selector
from jianjie.items import ShunqiAllItem


class TouzishijianSpider(scrapy.Spider):
	name = 'shunqi_all'
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
		start_url = "http://b2b.11467.com/"
		yield scrapy.Request(start_url)

	def parse(self, response):
		item = ShunqiAllItem()
		select = Selector(text=response.text)
		fas = select.xpath('//div[@class="box sidesubcat t5"]')
		for fa in fas:
			te = fa.xpath('./div[@class="boxtitle"]/text()').extract_first()
			if '按城市浏览全国公司黄页' != te:
				continue
			urls_a = fa.xpath('./div[@class="boxcontent"]/dl[@class="listtxt"]/dd/a')
			for a in urls_a:
				url = a.xpath('./@href').extract_first()
				url = urljoin(response.url, url)
				city = a.xpath('./em/text()').extract_first()
				item['city'] = city
				yield scrapy.Request(url, callback=self.parse_city, meta={'item': item})

	def parse_city(self, response):
		item = response.meta.get('item')
		sel = Selector(text=response.text)
		cat_tags = sel.xpath('//div[@class="boxcontent"]/ul[@class="listtxt"]/li/dl/dt/a')
		for cat_tag in cat_tags:
			cat_url = cat_tag.xpath('./@href').extract_first()
			yield scrapy.Request(cat_url, callback=self.parse_list, meta={'item': item})

	def parse_list(self, response):
		item = response.meta.get('item')
		sel = Selector(text=response.text)
		comp_urls = sel.xpath('//div[@class="f_l"]/h4/a/@href').extract()
		for comp_url in comp_urls:
			yield scrapy.Request('http:' + comp_url, callback=self.parse_detail, meta={'item': item})

		pn_next = sel.xpath('//div[@class="pages"]/a[text()="下一页"]/@href').extract_first()
		pn_last = sel.xpath('//div[@class="pages"]/a[text()="尾页"]/@href').extract_first()
		pn_ne = pn_next if pn_next else pn_last
		pn_nex = pn_ne if pn_ne else ''
		if not pn_nex:
			return
		yield scrapy.Request('http:' + pn_ne, callback=self.parse_list, meta={'item': item})

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
