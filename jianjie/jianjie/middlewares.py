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
from scrapy.exceptions import IgnoreRequest
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


class ProxyMiddleware(object):
	# 代理服务器
	proxyServer = "http://proxy.abuyun.com:9020"

	proxyUser = "H1PAC9C64710O54D"
	proxyPass = "2FBDED6DDC8FD140"

	# for Python3
	proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")

	def process_request(self, request, spider):
		request.meta["proxy"] = self.proxyServer
		request.headers["Proxy-Authorization"] = self.proxyAuth


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
