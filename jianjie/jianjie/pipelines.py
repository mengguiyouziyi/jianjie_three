# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from jianjie.items import Huangye88KunmingItem, Huangye88LiuzhouItem, ShunqiLiuzhouItem, ShunqiKunmingItem, \
	MinglujiLiuzhouItem, MinglujiKunmingItem, ShunqiAllItem, Huangye88AllItem, Huangye88AotuItem


class MysqlPipeline(object):
	def __init__(self):
		self.conn = pymysql.connect(host='172.31.215.38', port=3306, user='spider', password='spider', db='spider',
		                            charset='utf8', cursorclass=pymysql.cursors.DictCursor)
		self.cursor = self.conn.cursor()
		print('mysql init....')
		self.item_set = set()

	def process_item(self, item, spider):
		if isinstance(item, Huangye88KunmingItem):
			# sql = """insert into kuchuan_all(id, app_package, down, trend) VALUES(%s, %s, %s, %s) ON DUPLICATE KEY UPDATE app_package=VALUES(app_package), down=VALUES(down), down=VALUES(trend)"""
			sql = """insert into jianjie_huangye88_kunming (comp_url, comp_name, intro) VALUES(%s, %s, %s)"""
			args = [item['comp_url'], item['comp_name'], item['intro']]
			self.cursor.execute(sql, args)
			self.conn.commit()
		elif isinstance(item, Huangye88LiuzhouItem):
			sql = """insert into jianjie_huangye88_liuzhou (comp_url, comp_name, intro) VALUES(%s, %s, %s)"""
			args = [item['comp_url'], item['comp_name'], item['intro']]
			self.cursor.execute(sql, args)
			self.conn.commit()
		elif isinstance(item, ShunqiLiuzhouItem):
			sql = """insert into jianjie_shunqi_liuzhou (comp_url, comp_name, intro) VALUES(%s, %s, %s)"""
			args = [item['comp_url'], item['comp_name'], item['intro']]
			self.cursor.execute(sql, args)
			self.conn.commit()
		elif isinstance(item, ShunqiKunmingItem):
			sql = """insert into jianjie_shunqi_kunming (comp_url, comp_name, intro) VALUES(%s, %s, %s)"""
			args = [item['comp_url'], item['comp_name'], item['intro']]
			self.cursor.execute(sql, args)
			self.conn.commit()
		elif isinstance(item, MinglujiLiuzhouItem):
			sql = """insert into jianjie_mingluji_liuzhou (comp_url, comp_name, intro) VALUES(%s, %s, %s)"""
			args = [item['comp_url'], item['comp_name'], item['intro']]
			self.cursor.execute(sql, args)
			self.conn.commit()
		elif isinstance(item, MinglujiKunmingItem):
			sql = """insert into jianjie_mingluji_kunming (comp_url, comp_name, intro) VALUES(%s, %s, %s)"""
			args = [item['comp_url'], item['comp_name'], item['intro']]
			self.cursor.execute(sql, args)
			self.conn.commit()
		elif isinstance(item, ShunqiAllItem):
			if len(self.item_set) == 200:


				sql = """insert into jianjie_shunqi_all_copy (comp_url, comp_name, intro, city) VALUES(%s, %s, %s, %s)"""
				args_list = [[item['comp_url'], item['comp_name'], item['intro'], item['city']] for item in self.item_set]
				self.cursor.executemany(sql, args_list)
				self.conn.commit()
				self.item_set.clear()
				print('200 insert')


			else:
				self.item_set.add(item)
				print(str(item['comp_url']) + ' ' + str(item['comp_name']))



		elif isinstance(item, Huangye88AllItem):
			sql = """insert into jianjie_huangye88_all (comp_url, comp_name, intro, city) VALUES(%s, %s, %s, %s)"""
			args = [item['comp_url'], item['comp_name'], item['intro'], item['city']]
			self.cursor.execute(sql, args)
			self.conn.commit()
		elif isinstance(item, Huangye88AotuItem):
			sql = """insert into jianjie_huangye88_aotu (comp_url, comp_name, intro, posi, shengshi, cat) VALUES(%s, %s, %s, %s, %s, %s)"""
			args = [item['comp_url'], item['comp_name'], item['intro'], item['posi'], item['shengshi'], item['cat']]
			self.cursor.execute(sql, args)
			self.conn.commit()
		# print(str(item['comp_url']) + ' ' + str(item['comp_name']))
