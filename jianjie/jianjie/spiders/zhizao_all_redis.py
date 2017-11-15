# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin
from scrapy.selector import Selector
from jianjie.utils.bloomfilter import rc


class TouzishijianSpider(scrapy.Spider):
	name = 'zhizao_all_redis'
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
		start_url = "http://cn.made-in-china.com/gongsi/"
		yield scrapy.Request(start_url)

	def parse(self, response):
		select = Selector(text=response.text)
		cat_urls = select.xpath('//dl[contains(@class, "cata-item")]/dd/a/@href').extract()
		for cat_url in cat_urls:
			cat_url = urljoin(response.url, cat_url)
			rc.sadd('zhizao_all_caturl', cat_url)
			yield scrapy.Request(cat_url, callback=self.parse_cat)

	def parse_cat(self, response):
		sel = Selector(text=response.text)
		comp_urls = sel.xpath('//a[@class="more"]/@href').extract()
		for comp_url in comp_urls:
			comp_url = urljoin(response.url, comp_url)
			b_url = 'http://cn.made-in-china.com/showroom/'
			comp_id = comp_url.replace(b_url, '').replace('.cn.made-in-china.com', '').replace('http://', '')
			d_url = b_url + comp_id + "-companyinfo.html"
			rc.sadd('zhizao_all_detail', d_url)

		n_url = sel.xpath('//a[@class="page-next"]/@href').extract_first()
		if not n_url:
			return
		n_url = urljoin(response.url, n_url)
		rc.sadd('zhizao_all_caturl', n_url)
		yield scrapy.Request(n_url, callback=self.parse_cat)
