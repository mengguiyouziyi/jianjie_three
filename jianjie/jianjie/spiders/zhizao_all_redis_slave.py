# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.selector import Selector
from scrapy.exceptions import CloseSpider
from jianjie.items import ZhizaoAllItem
from jianjie.utils.bloomfilter import rc


class TouzishijianSpider(scrapy.Spider):
	name = 'shunqi_all_redis_slave'
	handle_httpstatus_list = [402]
	custom_settings = {
		'DEFAULT_REQUEST_HEADERS': {
			'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
			'accept-encoding': "gzip, deflate",
			'accept-language': "zh-CN,zh;q=0.8",
			'cache-control': "no-cache",
			'connection': "keep-alive",
			# 'cookie': "pid=zYuMTEwLjQxLjQyMjAxNzExMDIxNjU5MzcyNzI1NzE0NzY1NAM; sf_img=AM; JSESSIONID=abcpZzUpgXyIt-Dtr979v; bdshare_firstime=1510371528837; cn_com=jUxNDY3NDUyNiEsfjUyNTg3NDIyNiEsfjc3NDM4MDAyNiEsfjUwNzU4MjMyN; __utma=144487465.847166549.1509613180.1510379985.1510712090.5; __utmb=144487465.3.10.1510712090; __utmc=144487465; __utmz=144487465.1510712090.5.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; Hm_lvt_dcd77103e55fb7327c5d9c24690a3d89=1509613179,1510371331,1510712091; Hm_lpvt_dcd77103e55fb7327c5d9c24690a3d89=1510712633; cid=jAxNzExMDIxNjU5Mzg2MzEwMDAwNjAwOTAzMTQwOTE4MjYxNjkyM; sid=jAxNzExMDIxNjU5Mzg2MzEwMDA6MzYuMTEwLjQxLjQyM",
			'host': "cn.made-in-china.com",
			'referer': "http://cn.made-in-china.com/",
			'upgrade-insecure-requests': "1",
			# 'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
			'postman-token': "3a997115-2426-7b66-ecb5-59f64467a1af"
		}
	}

	def start_requests(self):
		# x = 0
		# while True:
		# 	comp_url = rc.spop('zhizao_all_detail')
		# 	if not comp_url:
		# 		x += 1
		# 		if x > 5:
		# 			raise CloseSpider('no datas')
		# 		time.sleep(60)
		# 		continue
		# 	yield scrapy.Request(comp_url)
		comp_url = 'http://cn.made-in-china.com/showroom/yanggang1232-companyinfo.html'
		yield scrapy.Request(comp_url)

	def parse(self, response):
		item = ZhizaoAllItem()
		comp_name = response.xpath('//div[@class="company-info"]//h1/text()|//div[@class="company-info"]//h2/text()|//div[@class="companyName-free clear"]//h2/text()').extract_first()
		intros = response.xpath('//p[@class="companyInf js-companyInf"]//text()').extract()
		intro = ''.join(intros) if intros else ''
		address = ''
		for select in response.xpath('//ul[@class="contactInfo"]/li'):
			context = select.xpath('./span[@class="contact-tit"]//text()').extract_first()
			if context and '地址' in context:
				address = select.xpath('./span[@class="contact-bd"]//text()').extract_first()
				address = address.replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', '')
				address = ''.join([x.strip() for x in address if x]) if address else ''

		item['comp_url'] = response.url
		item['comp_name'] = comp_name.trip() if comp_name else ''
		item['intro'] = intro
		item['addr'] = address

		yield item
