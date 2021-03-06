# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import hashlib
import time
# from scrapy.xlib.pydispatch import dispatcher
# from scrapy import signals
from scrapy.exceptions import DropItem, CloseSpider
from jianjie.items import Huangye88KunmingItem, Huangye88LiuzhouItem, ShunqiLiuzhouItem, ShunqiKunmingItem, \
	MinglujiLiuzhouItem, MinglujiKunmingItem, ShunqiAllItem, Huangye88AllItem, Huangye88AotuItem, WuyouAllItem, \
	huang114AllItem, ZhizaoAllItem, Ca800Item, JiqirenItem, ChuanItem


class MysqlPipeline(object):
	def __init__(self):
		self.conn = pymysql.connect(host='172.31.215.36', port=3306, user='base', password='imkloKuLiqNMc6Cn', db='innotree_data_project',
		                            charset='utf8', cursorclass=pymysql.cursors.DictCursor)
		self.cursor = self.conn.cursor()

	# self.item_list = []
	# dispatcher.connect(self.spider_closed, signals.spider_closed)

	# def __init__(self):
	#     self.browser = webdriver.Chrome(executable_path="D:/Temp/chromedriver.exe")
	#     super(JobboleSpider, self).__init__()
	#     dispatcher.connect(self.spider_closed, signals.spider_closed)
	#
	# def spider_closed(self, spider):
	# 	# 当爬虫退出的时候关闭chrome
	# 	print("spider closed")
	# 	sql = """insert into jianjie_shunqi_all_copy (comp_url, comp_name, intro, city) VALUES(%s, %s, %s, %s)"""
	# 	self.cursor.executemany(sql, self.item_list)
	# 	self.conn.commit()
	# 	print('%s insert' % len(self.item_list))

	def process_item(self, item, spider):
		if isinstance(item, Huangye88KunmingItem):
			# sql = """insert into kuchuan_all(id, app_package, down, trend) VALUES(%s, %s, %s, %s) ON DUPLICATE KEY UPDATE app_package=VALUES(app_package), down=VALUES(down), down=VALUES(trend)"""
			sql = """insert into jianjie_huangye88_kunming (comp_url, comp_name, intro) VALUES(%s, %s, %s)"""
			args = [item['comp_url'], item['comp_name'], item['intro']]
		elif isinstance(item, Huangye88LiuzhouItem):
			sql = """insert into jianjie_huangye88_liuzhou (comp_url, comp_name, intro) VALUES(%s, %s, %s)"""
			args = [item['comp_url'], item['comp_name'], item['intro']]
		elif isinstance(item, ShunqiLiuzhouItem):
			sql = """insert into jianjie_shunqi_liuzhou (comp_url, comp_name, intro) VALUES(%s, %s, %s)"""
			args = [item['comp_url'], item['comp_name'], item['intro']]
		elif isinstance(item, ShunqiKunmingItem):
			sql = """insert into jianjie_shunqi_kunming (comp_url, comp_name, intro) VALUES(%s, %s, %s)"""
			args = [item['comp_url'], item['comp_name'], item['intro']]
		elif isinstance(item, MinglujiLiuzhouItem):
			sql = """insert into jianjie_mingluji_liuzhou (comp_url, comp_name, intro) VALUES(%s, %s, %s)"""
			args = [item['comp_url'], item['comp_name'], item['intro']]
		elif isinstance(item, MinglujiKunmingItem):
			sql = """insert into jianjie_mingluji_kunming (comp_url, comp_name, intro) VALUES(%s, %s, %s)"""
			args = [item['comp_url'], item['comp_name'], item['intro']]
		elif isinstance(item, ShunqiAllItem):
			sql = """insert into jianjie_shunqi_all (comp_url, comp_name, intro, city) VALUES(%s, %s, %s, %s)"""
			args = [item['comp_url'], item['comp_name'], item['intro'], item['city']]
		# print(str(item['comp_url']) + ' ' + str(item['comp_name']))
		# if len(self.item_list) == 500:
		# 	sql = """insert into jianjie_shunqi_all_copy (comp_url, comp_name, intro, city) VALUES(%s, %s, %s, %s)"""
		# 	self.cursor.executemany(sql, self.item_list)
		# 	self.conn.commit()
		# 	self.item_list.clear()
		# 	print('200 insert')
		# else:
		# 	self.item_list.append([item['comp_url'], item['comp_name'], item['intro'], item['city']])
		elif isinstance(item, Huangye88AllItem):
			sql = """insert into jianjie_huangye88_all (comp_url, comp_name, intro, city) VALUES(%s, %s, %s, %s)"""
			args = [item['comp_url'], item['comp_name'], item['intro'], item['city']]
		elif isinstance(item, Huangye88AotuItem):
			sql = """insert into jianjie_huangye88_aotu (comp_url, comp_name, intro, posi, shengshi, cat) VALUES(%s, %s, %s, %s, %s, %s)"""
			args = [item['comp_url'], item['comp_name'], item['intro'], item['posi'], item['shengshi'], item['cat']]
		elif isinstance(item, WuyouAllItem):
			sql = """insert into jianjie_wuyou_all (comp_url, comp_name, intro, area) VALUES(%s, %s, %s, %s)"""
			args = [item['comp_url'], item['comp_name'], item['intro'], item['area']]
		elif isinstance(item, huang114AllItem):
			sql = """insert into jianjie_114_all_copy (comp_url, comp_name, link_man, tel, email, addr, intro) VALUES(%s, %s, %s, %s, %s, %s, %s)"""
			args = [item['comp_url'], item['comp_name'], item['link_man'], item['tel'], item['email'], item['addr'],
			        item['intro']]
		elif isinstance(item, ZhizaoAllItem):
			sql = """insert into jianjie_zhizao_all (comp_url, comp_name, addr, intro) VALUES(%s, %s, %s, %s)"""
			args = [item['comp_url'], item['comp_name'], item['addr'], item['intro']]
		elif isinstance(item, Ca800Item):
			sql = """insert into jianjie_ca800_all (comp_url, comp_name, cat_url, cat, loc, sheng, shi, intro) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""
			args = [item['comp_url'], item['comp_name'], item['cat_url'], item['cat'], item['loc'], item['sheng'], item['shi'], item['intro']]
		elif isinstance(item, JiqirenItem):
			sql = """insert into jianjie_jiqiren_all (zhuying, comp_url, comp_name, cat_url, cat, loc, sheng, shi, intro) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
			args = [item['zhuying'], item['comp_url'], item['comp_name'], item['cat_url'], item['cat'], item['loc'], item['sheng'], item['shi'], item['intro']]
		elif isinstance(item, JiqirenItem):
			sql = """insert into ChuanItem (zhuying, comp_url, comp_name, cat_url, cat, loc, sheng, shi, intro) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
			args = [item['zhuying'], item['comp_url'], item['comp_name'], item['cat_url'], item['cat'], item['loc'], item['sheng'], item['shi'], item['intro']]


		else:
			raise CloseSpider('no item match...')
		try:
			self.cursor.execute(sql, args)
			self.conn.commit()
			# print(str(item['comp_url']) + ' ' + str(item['comp_name']))
		except pymysql.err.InterfaceError:
			print('reconnect mysql...')
			time.sleep(3)
			self.__init__()
			self.process_item(item, spider)


class DuplicatesPipeline(object):
	def __init__(self):
		self.item_set = set()

	def process_item(self, item, spider):
		m = self.gen_md5(item['comp_url'])
		if m in self.item_set:
			raise DropItem("Duplicate item found")
		else:
			self.item_set.add(m)
			return item

	def gen_md5(self, comp_name):
		"""
		生成唯一id
		:return:
		0cc2662f5eb157c8ffcd43c145de499f2ab27a71
		72843135390705548651698998647502012318670289521
		a3f4a5b080e2a4ef4a708b9c9f5ad003
		217934444328053067635429399579879723011
		"""
		m = hashlib.md5()
		m.update(comp_name.encode('utf-8'))
		comp_md5 = m.hexdigest()
		# only_id_full = int(comp_md5, 16)
		# return str(only_id_full)
		return comp_md5
