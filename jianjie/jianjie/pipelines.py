# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from jianjie.items import Huangye88KunmingItem, Huangye88LiuzhouItem, ShunqiLiuzhouItem, ShunqiKunmingItem


class MysqlPipeline(object):
	def __init__(self):
		self.conn = pymysql.connect(host='etl1.innotree.org', port=3308, user='spider', password='spider', db='spider',
		                            charset='utf8', cursorclass=pymysql.cursors.DictCursor)
		self.cursor = self.conn.cursor()

	def process_item(self, item, spider):
		if isinstance(item, Huangye88KunmingItem):
			# sql = """insert into kuchuan_all(id, app_package, down, trend) VALUES(%s, %s, %s, %s) ON DUPLICATE KEY UPDATE app_package=VALUES(app_package), down=VALUES(down), down=VALUES(trend)"""
			sql = """insert into jianjie_huangye88_kunming (comp_url, comp_name, intro) VALUES(%s, %s, %s)"""
			args = [item['comp_url'], item['comp_name'], item['intro']]
			self.cursor.execute(sql, args)
			self.conn.commit()
			print(item['comp_url'] + item['comp_name'])
		elif isinstance(item, Huangye88LiuzhouItem):
			sql = """insert into jianjie_huangye88_liuzhou (comp_url, comp_name, intro) VALUES(%s, %s, %s)"""
			args = [item['comp_url'], item['comp_name'], item['intro']]
			self.cursor.execute(sql, args)
			self.conn.commit()
			print(item['comp_url'] + item['comp_name'])
		elif isinstance(item, ShunqiLiuzhouItem):
			sql = """insert into jianjie_shunqi_liuzhou (comp_url, comp_name, intro) VALUES(%s, %s, %s)"""
			args = [item['comp_url'], item['comp_name'], item['intro']]
			self.cursor.execute(sql, args)
			self.conn.commit()
			print(item['comp_url'] + item['comp_name'])
		elif isinstance(item, ShunqiKunmingItem):
			sql = """insert into jianjie_shunqi_kunming (comp_url, comp_name, intro) VALUES(%s, %s, %s)"""
			args = [item['comp_url'], item['comp_name'], item['intro']]
			self.cursor.execute(sql, args)
			self.conn.commit()
			print(item['comp_url'] + item['comp_name'])



