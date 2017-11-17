#coding:utf-8

import os
import sys

from scrapy.cmdline import execute

base_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(base_path)

execute(['scrapy', 'crawl', 'chuanganqi_all'])