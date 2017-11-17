# -*- coding: utf-8 -*-
import scrapy
import re
from urllib.parse import urljoin
from scrapy.selector import Selector
from jianjie.items import Ca800Item
from jianjie.utils.info import rc


class TouzishijianSpider(scrapy.Spider):
	name = 'ca800_master'

	# custom_settings = {
	# 	'DEFAULT_REQUEST_HEADERS': {
	# 		'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
	# 		'accept-encoding': "gzip, deflate",
	# 		'accept-language': "zh-CN,zh;q=0.8",
	# 		'cache-control': "no-cache",
	# 		# 'connection': "keep-alive",
	# 		# 'cookie': "ASP.NET_SessionId=kh5iqkvjtb4vjthzf40t54x1; cookiesmark=2017111717345000003; Hm_lvt_57a0c48ef04a2d3a7e7dec8e459b2bb4=1510911322; Hm_lpvt_57a0c48ef04a2d3a7e7dec8e459b2bb4=1510911380; sid=2017111717351400003; vid=2017111717351400004; _ga=GA1.2.332251248.1510911440; _gid=GA1.2.926593169.1510911440",
	# 		'host': "www.ca800.com",
	# 		'upgrade-insecure-requests': "1",
	# 		# 'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
	# 		# 'postman-token': "05eca74f-a731-dd48-9e85-fba7ae401bc6"
	# 	}
	# }

	def start_requests(self):
		start_urls = ["http://www.ca800.com/company/l_0_0_0_0_2_00_{}.html".format(i) for i in range(1, 9611)]
		for start_url in start_urls:
			rc.lpush('ca800_all', start_url)
