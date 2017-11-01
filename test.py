# class B(object):
# 	print('b')
#
#
# class D(object):
# 	print('d')


import hashlib


def gen_id(comp_name):
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
	print(comp_md5)
	only_id_full = int(comp_md5, 16)
	return str(only_id_full)


if __name__ == '__main__':
	only_id = gen_id('百度')
	print(only_id)

# # 导入selenium2中的webdriver库
# from selenium import webdriver
#
# # 实例化出一个Firefox浏览器
# driver = webdriver.Chrome(executable_path='/Users/menggui/.pyenv/versions/Anaconda3-4.3.0/bin/chromedriver')
#
# # 设置浏览器窗口的位置和大小
# driver.set_window_position(20, 40)
# driver.set_window_size(1100, 700)
#
# # 打开一个页面（QQ空间登录页）
# driver.get('http://qzone.qq.com')
# # 登录表单在页面的框架中，所以要切换到该框架
# driver.switch_to.frame('login_frame')
# # 通过使用选择器选择到表单元素进行模拟输入和点击按钮提交
# driver.find_element_by_id('switcher_plogin').click()
# driver.find_element_by_id('u').clear()
# driver.find_element_by_id('u').send_keys('944659889')
# driver.find_element_by_id('p').clear()
# driver.find_element_by_id('p').send_keys('sunlijian3646287')
# driver.find_element_by_id('login_button').click()
#
# # do something….
# # 退出窗口
# # driver.quit()
