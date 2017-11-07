# -*- coding: utf-8 -*-
import scrapy
import re
# from urllib.parse import urljoin
from scrapy.selector import Selector
from jianjie.items import WuyouAllItem


class TouzishijianSpider(scrapy.Spider):
	name = 'wuyou_all'
	custom_settings = {
		'DEFAULT_REQUEST_HEADERS': {
			'upgrade-insecure-requests': "1",
			# 'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
			'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
			'referer': "http://qiye.56ye.net/",
			'accept-encoding': "gzip, deflate",
			'accept-language': "zh-CN,zh;q=0.8",
			# 'cookie': "UM_distinctid=15f94f45fbb681-06f1de72f7e01a-31637e01-13c680-15f94f45fbcc9; firstEnterUrlInSession=http%3A//qiye.56ye.net/; VisitorCapacity=1; pageReferrInSession=http%3A//www.56ye.net/; CNZZDATA1266476=cnzz_eid%3D90178743-1510027475-http%253A%252F%252Fwww.56ye.net%252F%26ntime%3D1510027475; Hm_lvt_4cb5df180f862ce7696a758b27bd7fbd=1510032564; Hm_lpvt_4cb5df180f862ce7696a758b27bd7fbd=1510032718",
			'cache-control': "no-cache",
			'postman-token': "b3112c7b-bd87-6da2-070c-7d1a53a91745"
		}
	}

	def start_requests(self):
		area_list = ['北京', '上海', '天津', '重庆', '河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西', '山东',
		             '河南', '湖北', '湖南', '广东',
		             '广西', '海南', '四川', '贵州', '云南', '西藏', '陕西', '甘肃', '青海', '宁夏',
		             '新疆', '台湾', '香港', '澳门']
		for i in range(1, 35):
			yield scrapy.Request("http://qiye.56ye.net/search.php?areaid={area}&page=1".format(area=i),
			                     meta={'area': area_list[i-1]})

	def parse(self, response):
		area = response.meta.get('area')
		select = Selector(text=response.text)
		a_tags = select.xpath('//li[@class="sup-name"]/a[1]')
		print('a num', len(a_tags))
		for a in a_tags:
			# comp_name = a.xpath('./text()').extract_first()
			comp_url = a.xpath('./@href').extract_first()
			yield scrapy.Request(comp_url + 'introduce/', callback=self.parse_detail, meta={'area': area})

		p_num_list = select.xpath('//cite/text()').re(r'/(\d+)页$')
		# 注意最少是2页
		p_num = int(p_num_list[0]) if p_num_list else ''
		if not p_num:
			return
		url = response.url
		for n in range(2, p_num+1):
			# print('n', n)
			n_url = re.sub(r'\d+$', str(n), url)
			# print('send', n_url)
			yield scrapy.Request(n_url, callback=self.parse_next, meta={'area': area})

	def parse_next(self, response):
		# print('recieve', response.url)
		area = response.meta.get('area')
		select = Selector(text=response.text)
		a_tags = select.xpath('//li[@class="sup-name"]/a')
		for a in a_tags:
			# comp_name = a.xpath('./text()').extract_first()
			comp_url = a.xpath('./@href').extract_first()
			yield scrapy.Request(comp_url + 'introduce/', callback=self.parse_detail, meta={'area': area})

	def parse_detail(self, response):
		item = WuyouAllItem()
		area = response.meta.get('area')
		select = Selector(text=response.text)
		intro = select.xpath('//div[@class="main_body"]/div/table/tr/td//text()').extract()
		intro = ''.join(intro) if intro else ''
		comp_name = select.xpath('//div[@class="head"]/div/strong/text()').extract_first()
		item['comp_name'] = comp_name
		item['comp_url'] = response.url
		item['intro'] = intro
		item['area'] = area

		yield item
