import time


class A(object):
	def __init__(self):
		print(1)

	def f(self, num):
		print(num)
		time.sleep(3)
		self.__init__()
		self.f(num)


if __name__ == '__main__':
	a = A()
	a.f(2)

# import re
#
# url = 'http://www.11467.com/kunming/co/133281.htm'
# city = re.search(r'http://www\.11467\.com/(.*)/co/\d+.htm', url).group(1)
# print(city)


# import requests
# from urllib.parse import urljoin
# from scrapy import Selector
#
# url = "http://b2b.11467.com/"
#
# headers = {
# 	'x-devtools-emulate-network-conditions-client-id': "97d7041c-61b3-4087-907b-55cfcb08c429",
# 	'upgrade-insecure-requests': "1",
# 	'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
# 	'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
# 	'referer': "http://www.11467.com/kunming/",
# 	'accept-encoding': "gzip, deflate",
# 	'accept-language': "zh-CN,zh;q=0.8",
# 	'cookie': "Hm_lvt_819e30d55b0d1cf6f2c4563aa3c36208=1508817163; Hm_lpvt_819e30d55b0d1cf6f2c4563aa3c36208=1509343253",
# 	'cache-control': "no-cache",
# 	'postman-token': "42a3fd90-a2de-7f12-521b-53c5897f360e"
# }
#
# response = requests.request("GET", url, headers=headers)
#
# select = Selector(text=response.text)
# urls = select.xpath('//div[@class="boxcontent"]/dl[@class="listtxt"]/dd/a/@href').re(r'//www.11467.com/.*/$')
# urls = [urljoin(response.url, url) for url in urls]
# print(urls)
# start_urls = ['http://www.11467.com/shenzhen/', 'http://www.11467.com/guangzhou/', 'http://www.11467.com/dongguan/',
#               'http://www.11467.com/foshan/', 'http://www.11467.com/zhongshan/', 'http://www.11467.com/shantou/',
#               'http://www.11467.com/jiangmen/', 'http://www.11467.com/huizhou/', 'http://www.11467.com/zhuhai/',
#               'http://www.11467.com/zhanjiang/', 'http://www.11467.com/zhaoqing/', 'http://www.11467.com/maoming/',
#               'http://www.11467.com/chaozhou/', 'http://www.11467.com/jieyang/', 'http://www.11467.com/meizhou/',
#               'http://www.11467.com/qingyuan/', 'http://www.11467.com/shaoguan/', 'http://www.11467.com/yunfu/',
#               'http://www.11467.com/yangjiang/', 'http://www.11467.com/heyuan/', 'http://www.11467.com/shanwei/',
#               'http://www.11467.com/shanghai/', 'http://www.11467.com/beijing/', 'http://www.11467.com/chongqing/',
#               'http://www.11467.com/tianjin/', 'http://www.11467.com/suzhou/', 'http://www.11467.com/wuxi/',
#               'http://www.11467.com/nanjing/', 'http://www.11467.com/changzhou/', 'http://www.11467.com/nantong/',
#               'http://www.11467.com/yangzhou/', 'http://www.11467.com/xuzhou/', 'http://www.11467.com/yancheng/',
#               'http://www.11467.com/zhenjiang/', 'http://www.11467.com/taizhoushi/', 'http://www.11467.com/huaian/',
#               'http://www.11467.com/lianyungang/', 'http://www.11467.com/suqian/', 'http://www.11467.com/hangzhou/',
#               'http://www.11467.com/wenzhou/', 'http://www.11467.com/ningbo/', 'http://www.11467.com/jinhua/',
#               'http://www.11467.com/taizhou/', 'http://www.11467.com/jiaxing/', 'http://www.11467.com/shaoxing/',
#               'http://www.11467.com/huzhou/', 'http://www.11467.com/lishui/', 'http://www.11467.com/quzhou/',
#               'http://www.11467.com/zhoushan/', 'http://www.11467.com/yantai/', 'http://www.11467.com/weifang/',
#               'http://www.11467.com/qingdao/', 'http://www.11467.com/jinan/', 'http://www.11467.com/linyi/',
#               'http://www.11467.com/zibo/', 'http://www.11467.com/jining/', 'http://www.11467.com/liaocheng/',
#               'http://www.11467.com/dezhou/', 'http://www.11467.com/taian/', 'http://www.11467.com/weihai/',
#               'http://www.11467.com/heze/', 'http://www.11467.com/dongying/', 'http://www.11467.com/binzhou/',
#               'http://www.11467.com/zaozhuang/', 'http://www.11467.com/rizhao/', 'http://www.11467.com/laiwu/',
#               'http://www.11467.com/shijiazhuang/', 'http://www.11467.com/baoding/', 'http://www.11467.com/cangzhou/',
#               'http://www.11467.com/tangshan/', 'http://www.11467.com/handan/', 'http://www.11467.com/xintai/',
#               'http://www.11467.com/langfang/', 'http://www.11467.com/hengshui/', 'http://www.11467.com/qinhuangdao/',
#               'http://www.11467.com/zhangjiakou/', 'http://www.11467.com/chengde/', 'http://www.11467.com/fuzhou/',
#               'http://www.11467.com/quanzhou/', 'http://www.11467.com/xiamen/', 'http://www.11467.com/zhangzhou/',
#               'http://www.11467.com/putian/', 'http://www.11467.com/nanping/', 'http://www.11467.com/sanming/',
#               'http://www.11467.com/ningde/', 'http://www.11467.com/longyan/', 'http://www.11467.com/shenyang/',
#               'http://www.11467.com/dalian/', 'http://www.11467.com/anshan/', 'http://www.11467.com/dandong/',
#               'http://www.11467.com/jinzhou/', 'http://www.11467.com/yingkou/', 'http://www.11467.com/tieling/',
#               'http://www.11467.com/huludao/', 'http://www.11467.com/benxi/', 'http://www.11467.com/chaoyang/',
#               'http://www.11467.com/fushun/', 'http://www.11467.com/panjin/', 'http://www.11467.com/liaoyang/',
#               'http://www.11467.com/fuxin/', 'http://www.11467.com/chengdu/', 'http://www.11467.com/mianyang/',
#               'http://www.11467.com/deyang/', 'http://www.11467.com/yibin/', 'http://www.11467.com/nanchong/',
#               'http://www.11467.com/zigong/', 'http://www.11467.com/neijiang/', 'http://www.11467.com/luzhou/',
#               'http://www.11467.com/leshan/', 'http://www.11467.com/dazhou/', 'http://www.11467.com/guangyuan/',
#               'http://www.11467.com/panzhihua/', 'http://www.11467.com/meishan/', 'http://www.11467.com/liangshan/',
#               'http://www.11467.com/guangan/', 'http://www.11467.com/ziyang/', 'http://www.11467.com/suining/',
#               'http://www.11467.com/yaan/', 'http://www.11467.com/bazhong/', 'http://www.11467.com/aba/',
#               'http://www.11467.com/ganzi/', 'http://www.11467.com/zhengzhou/', 'http://www.11467.com/luoyang/',
#               'http://www.11467.com/nanyang/', 'http://www.11467.com/anyang/', 'http://www.11467.com/xinxiang/',
#               'http://www.11467.com/zhumadian/', 'http://www.11467.com/jiaozuo/', 'http://www.11467.com/zhoukou/',
#               'http://www.11467.com/xuchang/', 'http://www.11467.com/shangqiu/', 'http://www.11467.com/pingdingshan/',
#               'http://www.11467.com/puyang/', 'http://www.11467.com/xinyang/', 'http://www.11467.com/kaifeng/',
#               'http://www.11467.com/luohe/', 'http://www.11467.com/hebi/', 'http://www.11467.com/sanmenxia/',
#               'http://www.11467.com/hefei/', 'http://www.11467.com/anqing/', 'http://www.11467.com/fuyang/',
#               'http://www.11467.com/bengbu/', 'http://www.11467.com/wuhu/', 'http://www.11467.com/chuzhou/',
#               'http://www.11467.com/maanshan/', 'http://www.11467.com/xuancheng/', 'http://www.11467.com/suzhoushi/',
#               'http://www.11467.com/liuan/', 'http://www.11467.com/huainan/', 'http://www.11467.com/chaohu/',
#               'http://www.11467.com/huaibei/', 'http://www.11467.com/huangshan/', 'http://www.11467.com/bozhou/',
#               'http://www.11467.com/tongling/', 'http://www.11467.com/chizhou/', 'http://www.11467.com/wuhan/',
#               'http://www.11467.com/yichang/', 'http://www.11467.com/xiangfan/', 'http://www.11467.com/shiyan/',
#               'http://www.11467.com/jingzhou/', 'http://www.11467.com/xiaogan/', 'http://www.11467.com/huangshi/',
#               'http://www.11467.com/huanggang/', 'http://www.11467.com/jingmen/', 'http://www.11467.com/enshi/',
#               'http://www.11467.com/xianning/', 'http://www.11467.com/xiantao/', 'http://www.11467.com/ezhou/',
#               'http://www.11467.com/suizhou/', 'http://www.11467.com/tianmen/', 'http://www.11467.com/qianjiang/',
#               'http://www.11467.com/shenlongjia/', 'http://www.11467.com/changsha/', 'http://www.11467.com/zhuzhou/',
#               'http://www.11467.com/yueyang/', 'http://www.11467.com/changde/', 'http://www.11467.com/hengyang/',
#               'http://www.11467.com/shaoyang/', 'http://www.11467.com/xiangtan/', 'http://www.11467.com/chenzhou/',
#               'http://www.11467.com/huaihua/', 'http://www.11467.com/yiyang/', 'http://www.11467.com/yongzhou/',
#               'http://www.11467.com/loudi/', 'http://www.11467.com/xianxi/', 'http://www.11467.com/zhangjiajie/',
#               'http://www.11467.com/haerbin/', 'http://www.11467.com/qiqihaer/', 'http://www.11467.com/mudanjiang/',
#               'http://www.11467.com/daqing/', 'http://www.11467.com/jiamusi/', 'http://www.11467.com/jixi/',
#               'http://www.11467.com/heihe/', 'http://www.11467.com/suihua/', 'http://www.11467.com/yichunshi/',
#               'http://www.11467.com/hegang/', 'http://www.11467.com/shuangyashang/', 'http://www.11467.com/qitaihe/',
#               'http://www.11467.com/daxinganling/', 'http://www.11467.com/taiyuan/', 'http://www.11467.com/linfen/',
#               'http://www.11467.com/changzhi/', 'http://www.11467.com/yuncheng/', 'http://www.11467.com/jinzhong/',
#               'http://www.11467.com/lvliang/', 'http://www.11467.com/jincheng/', 'http://www.11467.com/xinzhou/',
#               'http://www.11467.com/datong/', 'http://www.11467.com/yangquan/', 'http://www.11467.com/shuozhou/',
#               'http://www.11467.com/jilinshi/', 'http://www.11467.com/changchun/', 'http://www.11467.com/yanbian/',
#               'http://www.11467.com/siping/', 'http://www.11467.com/tonghua/', 'http://www.11467.com/baicheng/',
#               'http://www.11467.com/songyuan/', 'http://www.11467.com/baishan/', 'http://www.11467.com/liaoyuan/',
#               'http://www.11467.com/nanning/', 'http://www.11467.com/guilin/', 'http://www.11467.com/liuzhou/',
#               'http://www.11467.com/yulin/', 'http://www.11467.com/wuzhou/', 'http://www.11467.com/beihai/',
#               'http://www.11467.com/baise/', 'http://www.11467.com/hechi/', 'http://www.11467.com/qinzhou/',
#               'http://www.11467.com/guigang/', 'http://www.11467.com/fangchenggang/', 'http://www.11467.com/hezhou/',
#               'http://www.11467.com/chongzuo/', 'http://www.11467.com/laibin/', 'http://www.11467.com/nanchang/',
#               'http://www.11467.com/ganzhou/', 'http://www.11467.com/shangrao/', 'http://www.11467.com/jiujiang/',
#               'http://www.11467.com/yichun/', 'http://www.11467.com/jian/', 'http://www.11467.com/fuzhoushi/',
#               'http://www.11467.com/pingxiang/', 'http://www.11467.com/jingdezhen/', 'http://www.11467.com/xinyu/',
#               'http://www.11467.com/yingtan/', 'http://www.11467.com/xian/', 'http://www.11467.com/baoji/',
#               'http://www.11467.com/xianyang/', 'http://www.11467.com/weinan/', 'http://www.11467.com/hanzhong/',
#               'http://www.11467.com/yulinshi/', 'http://www.11467.com/yanan/', 'http://www.11467.com/ankang/',
#               'http://www.11467.com/shangluo/', 'http://www.11467.com/tongchuan/', 'http://www.11467.com/kunming/',
#               'http://www.11467.com/qujing/', 'http://www.11467.com/honghe/', 'http://www.11467.com/yuxi/',
#               'http://www.11467.com/chuxiong/', 'http://www.11467.com/dali/', 'http://www.11467.com/zhaotong/',
#               'http://www.11467.com/baoshan/', 'http://www.11467.com/puer/', 'http://www.11467.com/wenshan/',
#               'http://www.11467.com/lincang/', 'http://www.11467.com/lijiang/', 'http://www.11467.com/xishuangbanna/',
#               'http://www.11467.com/dehong/', 'http://www.11467.com/nujiang/', 'http://www.11467.com/diqing/',
#               'http://www.11467.com/wulumuqi/', 'http://www.11467.com/bayinguoleng/', 'http://www.11467.com/changji/',
#               'http://www.11467.com/yili/', 'http://www.11467.com/akesu/', 'http://www.11467.com/kashi/',
#               'http://www.11467.com/kelamayi/', 'http://www.11467.com/tacheng/', 'http://www.11467.com/shihezi/',
#               'http://www.11467.com/aletai/', 'http://www.11467.com/hetian/', 'http://www.11467.com/hami/',
#               'http://www.11467.com/tulufan/', 'http://www.11467.com/boerdala/', 'http://www.11467.com/kezilesu/',
#               'http://www.11467.com/wujiaqu/', 'http://www.11467.com/alaer/', 'http://www.11467.com/tumushuke/',
#               'http://www.11467.com/lanzhou/', 'http://www.11467.com/qingyang/', 'http://www.11467.com/tianshui/',
#               'http://www.11467.com/jiuquan/', 'http://www.11467.com/zhangye/', 'http://www.11467.com/wuwei/',
#               'http://www.11467.com/dingxi/', 'http://www.11467.com/longnan/', 'http://www.11467.com/pingliang/',
#               'http://www.11467.com/baiyin/', 'http://www.11467.com/linxia/', 'http://www.11467.com/jinchang/',
#               'http://www.11467.com/gannan/', 'http://www.11467.com/jiayuguan/', 'http://www.11467.com/guiyang/',
#               'http://www.11467.com/zunyi/', 'http://www.11467.com/qiandongnan/', 'http://www.11467.com/liupanshui/',
#               'http://www.11467.com/qiannan/', 'http://www.11467.com/bijie/', 'http://www.11467.com/anshun/',
#               'http://www.11467.com/tongren/', 'http://www.11467.com/qianxinan/', 'http://www.11467.com/huhehaote/',
#               'http://www.11467.com/baotou/', 'http://www.11467.com/chifeng/', 'http://www.11467.com/hulunbeier/',
#               'http://www.11467.com/tongliao/', 'http://www.11467.com/eerduosi/', 'http://www.11467.com/xingan/',
#               'http://www.11467.com/wulanchabu/', 'http://www.11467.com/bayannaoer/', 'http://www.11467.com/wuhai/',
#               'http://www.11467.com/xilinguole/', 'http://www.11467.com/alashan/', 'http://www.11467.com/erlianhaote/',
#               'http://www.11467.com/manzhouli/', 'http://www.11467.com/yinchuan/', 'http://www.11467.com/shizuishan/',
#               'http://www.11467.com/wuzhong/', 'http://www.11467.com/guyuan/', 'http://www.11467.com/zhongwei/',
#               'http://www.11467.com/xining/', 'http://www.11467.com/haixi/', 'http://www.11467.com/haidong/',
#               'http://www.11467.com/huangnan/', 'http://www.11467.com/haibei/', 'http://www.11467.com/qhhainan/',
#               'http://www.11467.com/guoluo/', 'http://www.11467.com/yushu/', 'http://www.11467.com/lasa/',
#               'http://www.11467.com/rikaze/', 'http://www.11467.com/changdu/', 'http://www.11467.com/shannan/',
#               'http://www.11467.com/naqu/', 'http://www.11467.com/ali/', 'http://www.11467.com/linzhi/',
#               'http://www.11467.com/haikou/', 'http://www.11467.com/sanya/', 'http://www.11467.com/shanzhou/',
#               'http://www.11467.com/qionghai/', 'http://www.11467.com/wanning/', 'http://www.11467.com/wenchang/',
#               'http://www.11467.com/chengmai/', 'http://www.11467.com/dongfang/', 'http://www.11467.com/anding/',
#               'http://www.11467.com/changjiang/', 'http://www.11467.com/lingao/', 'http://www.11467.com/qiongzhong/',
#               'http://www.11467.com/tunchang/', 'http://www.11467.com/baoting/', 'http://www.11467.com/baisha/',
#               'http://www.11467.com/yuedong/', 'http://www.11467.com/lingshui/', 'http://www.11467.com/wuzhishan/',
#               'http://www.11467.com/sanshashi/', 'http://www.11467.com/yangpu/']
