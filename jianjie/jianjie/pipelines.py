# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from jianjie.items import Huangye88KunmingItem


class MysqlPipeline(object):
	def __init__(self):
		self.conn = pymysql.connect(host='etl2.innotree.org', port=3308, user='spider', password='spider', db='spider',
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


			# elif isinstance(item, TzjgItem):
			# 	sql = """insert into touzijie_touzijigou (tz_jg_detail,tz_jg_logo,tz_jg_name,tz_jg_short,tz_jg_en,capital_type,tz_jg_property,tz_jg_regist_addr,tz_jg_create_time,tz_jg_headquarter,tz_jg_site,tz_jg_invest_stage,tz_jg_intro,tz_jg_tel,tz_jg_fax,tz_jg_addr,tz_jg_postcode,team_per_list,tz_sj_url,tz_sj_list,mz_sj_url,mz_sj_list) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
			# 	args = [item['tz_jg_detail'], item['tz_jg_logo'], item['tz_jg_name'], item['tz_jg_short'], item['tz_jg_en'],
			# 	        item['capital_type'],
			# 	        item['tz_jg_property'], item['tz_jg_regist_addr'], item['tz_jg_create_time'],
			# 	        item['tz_jg_headquarter'], item['tz_jg_site'], item['tz_jg_invest_stage'], item['tz_jg_intro'],
			# 	        item['tz_jg_tel'], item['tz_jg_fax'], item['tz_jg_addr'], item['tz_jg_postcode'],
			# 	        item['team_per_list'], item['tz_sj_url'], item['tz_sj_list'], item['mz_sj_url'], item['mz_sj_list']]
			# 	self.cursor.execute(sql, args)
			# 	self.conn.commit()
			# 	print(item['tz_jg_detail'])
			# elif isinstance(item, RzgsItem):
			# 	sql = """insert into touzijie_rongzigongsi (rz_gs_detail,rz_gs_logo,rz_gs_name,rz_gs_short,rz_gs_en,rz_gs_headquarter,rz_gs_regist_addr,rz_gs_create_time,rz_gs_industry,rz_gs_site,rz_gs_intro,rz_gs_fax,rz_gs_tel,rz_gs_postcode,rz_gs_addr,rz_sj_list) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
			# 	args = [item['rz_gs_detail'], item['rz_gs_logo'], item['rz_gs_name'], item['rz_gs_short'], item['rz_gs_en'],
			# 	        item['rz_gs_headquarter'], item['rz_gs_regist_addr'], item['rz_gs_create_time'],
			# 	        item['rz_gs_industry'], item['rz_gs_site'], item['rz_gs_intro'], item['rz_gs_fax'],
			# 	        item['rz_gs_tel'], item['rz_gs_postcode'], item['rz_gs_addr'], item['rz_sj_list']
			# 	        ]
			# 	self.cursor.execute(sql, args)
			# 	self.conn.commit()
			# 	print(item['rz_gs_detail'])
			# if isinstance(item, MzsjItem):
			# 	sql = """insert into touzijie_muzishijian (mz_sj_detail,mz_sj_title,mz_fund_name,currency,mz_sj_create_time,mz_sj_state,tz_jg_detail,tz_jg_name,target_size,capital_type,mz_sj_money,prospectus_intro) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
			# 	args = [
			# 		item['mz_sj_detail'], item['mz_sj_title'], item['mz_fund_name'], item['currency'],
			# 		item['mz_sj_create_time'], item['mz_sj_state'], item['tz_jg_detail'], item['tz_jg_name'],
			# 		item['target_size'], item['capital_type'], item['mz_sj_money'], item['prospectus_intro']]
			# 	self.cursor.execute(sql, args)
			# 	self.conn.commit()
			# 	print(item['mz_sj_detail'])
			# if isinstance(item, SssjItem):
			# 	sql = """insert into touzijie_shangshishijian (ss_sj_detail,ss_sj_title,rz_gs_detail,rz_gs_name,rz_gs_industry_url,rz_gs_industry,rz_gs_ipo_time,tz_jg_name,rz_gs_issue_price,rz_gs_ipo_addr_url,rz_gs_ipo_addr,rz_gs_sirculation,rz_gs_stock_code,is_support) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
			# 	args = [
			# 		item['ss_sj_detail'], item['ss_sj_title'], item['rz_gs_detail'], item['rz_gs_name'],
			# 		item['rz_gs_industry_url'], item['rz_gs_industry'], item['rz_gs_ipo_time'], item['tz_jg_name'],
			# 		item['rz_gs_issue_price'], item['rz_gs_ipo_addr_url'], item['rz_gs_ipo_addr'],
			# 		item['rz_gs_sirculation'], item['rz_gs_stock_code'], item['is_support']
			# 	]
			# 	self.cursor.execute(sql, args)
			# 	self.conn.commit()
			# 	print(item['ss_sj_detail'])
			# if isinstance(item, BgsjItem):
			# 	sql = """insert into touzijie_binggoushijian (bg_sj_detail,bg_sj_title,bg_gs_detail,bg_gs_name,bei_bg_gs_detail,bei_bg_gs_name,bg_state,industry_url,industry,equity_concern,bg_start_time,bg_finish_time,is_support,bg_sj_intro) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
			# 	args = [
			# 		item['bg_sj_detail'], item['bg_sj_title'], item['bg_gs_detail'], item['bg_gs_name'],
			# 		item['bei_bg_gs_detail'], item['bei_bg_gs_name'], item['bg_state'], item['industry_url'],
			# 		item['industry'], item['equity_concern'], item['bg_start_time'], item['bg_finish_time'],
			# 		item['is_support'], item['bg_sj_intro']
			# 	]
			# 	self.cursor.execute(sql, args)
			# 	self.conn.commit()
			# 	print(item['bg_sj_detail'])
