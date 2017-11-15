# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import os
import sys
from os.path import dirname

father_path = dirname(dirname(os.path.abspath(dirname(__file__))))
base_path = dirname(dirname(os.path.abspath(dirname(__file__))))
path = dirname(os.path.abspath(dirname(__file__)))
sys.path.append(path)
sys.path.append(base_path)
sys.path.append(father_path)

import base64
from random import choice
from scrapy.exceptions import IgnoreRequest, CloseSpider


# from jianjie.utils.bloomfilter import PyBloomFilter, rc


# class BloomfilterMiddleware(object):
# 	def __init__(self):
# 		self.bf = PyBloomFilter(conn=rc)
#
# 	def process_request(self, request, spider):
# 		url = request.url
# 		if self.bf.is_exist(url):
# 			raise IgnoreRequest
# 		else:
# 			self.bf.add(url)

class CloseMiddleware(object):
	def process_response(self, request, response, spider):
		if response.status == 402:
			raise CloseSpider('402 proxy no use')
		else:
			return response


class ProxyMiddleware(object):
	def __init__(self):
		self.proxyServer = "http://proxy.abuyun.com:9020"
		pl = [
			"HJ3F19379O94DO9D:D1766F5002A70BC4",
			# "H285292O32R01G0D:1DA6335539C2EB5F",
			# "HD3920957396Y39D:9E33CB0DEAD0A6E7",
			# "HH8W3B5VNSU81V6D:77D96A7DC3F52766",
			# "H334A990UYU4UKLD:628E84E1535E7F42",
			# "H1PAC9C64710O54D:2FBDED6DDC8FD140",
			# "HG6V4272626N007D:C08BB93CF91E2391",
			# "HY5ZDUG5F9F2194D:245205A0461BDE12",
			# "H51144995KA6IC8D:E0F0E2F2B96DED0F",
			# "HMQFU126826U5J7D:176550D703FA05E4",
			# "H34C100W441WVO6D:A3CD5352C2863367",
		]
		self.proxyAuths = ["Basic " + base64.urlsafe_b64encode(bytes(p, "ascii")).decode("utf8") for p in pl]

	def process_request(self, request, spider):
		request.meta["proxy"] = self.proxyServer
		request.headers["Proxy-Authorization"] = choice(self.proxyAuths)


class RetryMiddleware(object):
	def process_response(self, request, response, spider):
		if response.status in [429, 503]:
			# print('wrong status: %s, retrying~~' % response.status, request.url)
			retryreq = request.copy()
			retryreq.dont_filter = True
			return retryreq
		else:
			return response


class RotateUserAgentMiddleware(object):
	"""Middleware used for rotating user-agent for each request"""

	def __init__(self, agents):
		self.agents = agents

	@classmethod
	def from_crawler(cls, crawler):
		return cls(crawler.settings.get('USER_AGENT_CHOICES', []))

	def process_request(self, request, spider):
		request.headers.setdefault('User-Agent', choice(self.agents))
