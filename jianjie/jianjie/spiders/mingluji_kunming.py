# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from urllib.parse import urljoin
from jianjie.items import MinglujiKunmingItem


class TouzishijianSpider(scrapy.Spider):
	name = 'mingluji_kunming'
	custom_settings = {
		'DEFAULT_REQUEST_HEADERS': {
			'upgrade-insecure-requests': "1",
			# 'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
			'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
			'accept-encoding': "gzip, deflate, br",
			'accept-language': "zh-CN,zh;q=0.8",
			# 'cookie': "__utma=174508724.1927857987.1508835834.1508835834.1508835834.1; __utmb=174508724.9.10.1508835834; __utmc=174508724; __utmz=174508724.1508835834.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); Hm_lvt_f733651f7f7c9cfc0c1c62ebc1f6388e=1508835834; Hm_lpvt_f733651f7f7c9cfc0c1c62ebc1f6388e=1508836248",
			'cache-control': "no-cache",
			'postman-token': "b49199e9-e9b8-546b-7342-5339b0048df4"
		}
	}

	def start_requests(self):
		start_url = "https://guangxi.mingluji.com/%E6%9F%B3%E5%B7%9E%E5%B8%82"
		yield scrapy.Request(start_url)

	def parse(self, response):
		sel = Selector(text=response.text)
		comp_urls = sel.xpath('//div[@id="mw-content-text"]/table/tr/td/ol/li/a/@href').extract()
		for comp_url in comp_urls:
			yield scrapy.Request(urljoin(response.url, comp_url), callback=self.parse_detail)
		pn_next = sel.xpath('//div[@id="mw-content-text"]/table/tr/td/dl/dd/a[text()="后一页 ▽"]/@href').extract_first()
		print(pn_next)
		if not pn_next:
			return
		yield scrapy.Request(urljoin(response.url, pn_next))

	def parse_detail(self, response):
		item = MinglujiKunmingItem()
		sel = Selector(text=response.text)
		comp_name = sel.xpath('//span[@itemprop="name"]/text()').extract_first()
		intros = sel.xpath('//span[@itemprop="description"]/text()').extract()
		intro = ''.join(intros) if intros else ''
		intro = intro.strip()
		item['comp_url'] = response.url
		item['comp_name'] = comp_name
		item['intro'] = intro

		yield item
