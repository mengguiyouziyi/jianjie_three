# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import base64
from random import choice


class ProxyMiddleware(object):
	# 代理服务器
	proxyServer = "http://proxy.abuyun.com:9020"

	# 1
	# proxyUser = "HE5I6A6073H102ID"
	# proxyPass = "48512F15BA217F88"

	proxyUser = "HJ6L850B9KJ69Y4D"
	proxyPass = "6B572FD15BBDC0E9"

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
