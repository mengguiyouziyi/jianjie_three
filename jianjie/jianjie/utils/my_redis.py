# -*- coding: utf-8 -*-
import redis, time
# from lagou import settings

import os
import sys
from os.path import dirname

father_path = dirname(os.path.abspath(dirname(__file__)))
sys.path.append(father_path)

UNIQ_REDIS_HOST = 'a027.hb2.innotree.org'
UNIQ_REDIS_PORT = 6379
QUEUE_REDIS_HOST = 'a027.hb2.innotree.org'
# QUEUE_REDIS_HOST = 'localhost'
QUEUE_REDIS_PORT = 6379


class Singleton(object):
	def __new__(cls, *args, **kw):
		if not hasattr(cls, '_instance'):
			orig = super(Singleton, cls)
			cls._instance = orig.__new__(cls, *args, **kw)
		return cls._instance


class UniqRedis(Singleton):
	'''@ 此处采用单列模式，
	   @ 避免过多的实例化。
		'''
	try:
		pool = redis.ConnectionPool(host=UNIQ_REDIS_HOST, port=UNIQ_REDIS_PORT)
		__db = redis.StrictRedis(connection_pool=pool, decode_responses=True)
	except Exception as e:
		print(e)

	def conn(self):
		return self.__db

	def uniq(self, key):
		'''@ 去重，连接池方式，直接把key
		   @ 搁置在顶层目录不妥
			'''
		if self.__db.get(key):
			return True
		return False

	"""
	def count(self, key):
		'''@ 统计，连接池方式，连接较频繁，
		   @ 下载量，真实下载量，重复数据量，解析失败数据量
		   @ incr: 递增
			'''
		current_crawl_count = "%s%s_%s" % (settings.SERVER_FLAG, key, time.strftime("%Y_%m_%d_%H", time.localtime()))
		self.__db.incr(current_crawl_count)

	def get_count_result(self, key):
		'''@ 获取统计结果
		   @ key: 需统计的key
			'''
		count = self.__db.get(key)
		print "%s: %s" % (key, count)
	"""


class QueueRedis(Singleton):
	try:
		pool = redis.ConnectionPool(host=QUEUE_REDIS_HOST, port=QUEUE_REDIS_PORT)
		__db = redis.StrictRedis(connection_pool=pool, decode_responses=True)
	except Exception as e:
		print(e)

	def read_from_queue(self, queueName, count):
		results = []
		for index in range(0, count):
			item = self.__dequeue(queueName)
			if item:
				results.append(item)
			else:
				return results
		return results

	def send_to_queue(self, queueName, message):
		self.__enqueue(queueName, message)

	def get_queue_length(self, queueName):
		return self.__db.llen(queueName)

	def __dequeue(self, queueName, block=False, timeout=3):
		"""出队
			"""
		try:
			if block:
				return self.__db.blpop(queueName, timeout=timeout)
			return self.__db.lpop(queueName)
		except Exception as e:
			print(e)
		return None

	def __enqueue(self, queueName, message):
		"""入队
			"""
		try:
			self.__db.rpush(queueName, message)
		except Exception as e:
			print(e)
