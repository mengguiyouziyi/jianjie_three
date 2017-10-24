import requests
import re
import pymysql
import traceback
import time
from math import ceil
from urllib.parse import urljoin
from scrapy import Selector


def get_res(url):
	headers = {
		'x-devtools-emulate-network-conditions-client-id': "82dfd7c8-61b5-4d6e-be6b-737478ed94c1",
		'upgrade-insecure-requests': "1",
		'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
		'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
		'referer': "http://b2b.huangye88.com/yunnan/",
		'accept-encoding': "gzip, deflate",
		'accept-language': "zh-CN,zh;q=0.8",
		'cookie': "PHPSESSID=4040d366a1b443148ac52884266bed3659eeb167d63461.93983296; _ga=GA1.2.1756847603.1508815209; _gid=GA1.2.343721429.1508815209; Hm_lvt_c8184fd80a083199b0e82cc431ab6740=1508815209; Hm_lpvt_c8184fd80a083199b0e82cc431ab6740=1508815666",
		'cache-control': "no-cache",
		'postman-token': "41f85de8-6890-17d4-f427-410383245168"
	}

	response = requests.request("GET", url, headers=headers)
	# time.sleep(0.5)
	return response


def parse(base_url, cate, page=1):
	response = get_res(base_url.format(cate, page))
	select = Selector(text=response.text)
	item_tags = select.xpath('//dl[@class="col-dl"]')
	for item_tag in item_tags:
		name_tag = item_tag.xpath('./dt[@class="h2"]/a')
		item_url_un = name_tag.xpath('./@href').extract_first()
		item_url = urljoin(response.url, item_url_un)
		name = name_tag.xpath('./text()').extract_first()
		creat_tag = item_tag.xpath('./dd[@class="gray "][1]')
		creat_time = creat_tag.xpath('./text()').extract()[1]
		creat_per_url_un = creat_tag.xpath('./a/@href').extract_first()
		creat_per_url = urljoin(response.url, creat_per_url_un)
		creat_per = creat_tag.xpath('./a/text()').extract_first()
		tag_tags = item_tag.xpath('./dd[2]/a')
		tags = []
		for tag_tag in tag_tags:
			tag_url_un = tag_tag.xpath('./@href').extract_first()
			tag_url = urljoin(response.url, tag_url_un)
			tag = tag_tag.xpath('./text()').extract_first()
			tag_dict = {'tag_url': tag_url, 'tag': tag}
			tags.append(tag_dict)
		sumry = item_tag.xpath('./dd[3]/p/text()').extract_first()
		edit_scan = item_tag.xpath('./dd[@class="gray "][2]/text()').extract_first()
		person_dict = {'item_url': item_url, 'name': name, 'creat_time': creat_time, 'creat_per_url': creat_per_url,
		               'creat_per': creat_per, 'tags': to_str(tags), 'sumry': sumry, 'edit_scan': edit_scan}

		detail_dict = parse_detail(item_url)
		person_dict.update(detail_dict)

		# 入库
		etl_config = {'host': 'etl2.innotree.org',
		              'port': 3308,
		              'user': 'spider',
		              'password': 'spider',
		              'db': 'spider',
		              'charset': 'utf8',
		              'cursorclass': pymysql.cursors.DictCursor}
		con = pymysql.connect(**etl_config)
		try:
			in_mysql(con, person_dict)
		except:
			traceback.print_exc()
		finally:
			con.close()

	# print(item_url)
	# print(name)
	# print(creat_time)
	# print(creat_per_url)
	# print(creat_per)
	# print(tags)
	# print(sumry)
	# print(edit_scan)

	# print(late_edit_url)
	# print(late_edit)
	# print(update_time)
	# print(item_detail)
	# print(img_list)
	# print(contents)
	# print(reference_list)

	# 申请下一页
	item_num = re.search(r'\d+', select.xpath('//h2[@class="col-h2 h3 a-r"]/text()').extract_first()).group()
	p_num = ceil(int(item_num) / 10)
	now_page = int(re.search(r'\d+$', response.url).group())
	if now_page >= p_num:
		return
	parse(base_url, cate, now_page + 1)


def parse_detail(item_url):
	# 详情页申请
	res_detail = get_res(item_url)
	sel_detail = Selector(text=res_detail.text)

	dl_tags = sel_detail.xpath('//dl[@class="col-dl twhp2"]').extract()
	late_edit_url = ''
	late_edit = ''
	if len(dl_tags) >= 2:
		late_edit_tag = sel_detail.xpath('//dl[@class="col-dl twhp2"][2]/dt/a')
		late_edit_url_un = late_edit_tag.xpath('./@href').extract_first()
		late_edit_url = urljoin(res_detail.url, late_edit_url_un)
		late_edit = late_edit_tag.xpath('./text()').extract_first()
	update_time = sel_detail.xpath('//ul[@class="col-ul bor-ccc"]/li[last()]/text()').extract_first()
	item_detail_tag = sel_detail.xpath('//div[@class="content_1 wordcut"]')
	item_detail = item_detail_tag.extract_first()

	all_list = item_detail_tag.xpath(
		'./h3/span/text()|./div[@class="content_topp"]/p/text()|./div[@class="content_topp"]/text()').extract()
	contents = ''.join(all_list)
	# print(contents)
	# print()
	# h3s = item_detail_tag.xpath('./h3/span/text()').extract()
	# print(h3s)
	# if len(h3s) > 0:
	# 	del h3s[0]
	content_tags = item_detail_tag.xpath('./div[@class="content_topp"]')
	# for co in content_tags:
	# 	print(co.extract())
	# 	print()
	# content_tag__ = item_detail_tag.xpath('./div[@class="content_topp"]/text()|./div[@class="content_topp"]/p/text()').extract()
	# print(content_tag__)
	img_list = []
	for content_tag in content_tags:
		img_un = content_tag.xpath(
			'./div[@class="img img_l"]/a/@href|./div[@class="img img_r"]/a/@href').extract_first()
		if not img_un:
			continue
		img = urljoin(res_detail.url, img_un) if img_un else ''
		img_list.append(img)
	reference_tags = sel_detail.xpath('//*[@id="reference_view"]/dd')
	reference_list = []
	for reference_tag in reference_tags:
		reference_name_list = reference_tag.xpath('./text()').extract()
		reference_name = ''.join(reference_name_list).replace(u'\xa0', '').strip() if reference_name_list else ''
		reference_url = reference_tag.xpath('./span[2]/text()').extract_first()
		reference_dict = {'reference_name': reference_name, 'reference_url': reference_url}
		reference_list.append(reference_dict)
	cat_tags = sel_detail.xpath('//*[@id="catenavi"]/a')
	cat = []
	for cat_tag in cat_tags:
		cat_url_un = cat_tag.xpath('./@href').extract_first()
		cat_url = urljoin(res_detail.url, cat_url_un)
		cat_name = cat_tag.xpath('./text()').extract_first()
		cat_dict = {'cat_url': cat_url, 'cat_name': cat_name}
		cat.append(cat_dict)
	return {'late_edit_url': late_edit_url, 'late_edit': late_edit, 'update_time': update_time,
	        'item_detail': item_detail, 'img_list': to_str(img_list), 'contents': contents,
	        'reference_list': to_str(reference_list),
	        'cat': to_str(cat)}


def in_mysql(con, dic):
	sql = """insert into qianren_jihua (item_url, per_name, creat_time, creat_per_url, creat_per, tags, sumry, edit_scan, late_edit_url, late_edit, update_time, item_detail, img_list, contents, reference_list, cat) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
	print(sql)
	spider_cur = con.cursor()
	print(list(dic.values()))
	spider_cur.execute(sql, list(dic.values()))
	con.commit()


def to_str(li):
	return str(li) if li else ''


if __name__ == '__main__':
	cates = list(range(13, 22))
	cates.append(23)

	url = "http://www.1000plan.org/wiki/index.php?category-view-{}-{}"
	for cate in cates:
		parse(url, cate)
