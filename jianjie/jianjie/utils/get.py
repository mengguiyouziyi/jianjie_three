# coding:utf-8

import os
import sys
from os.path import dirname

father_path = os.path.abspath(dirname(__file__))
sys.path.append(father_path)

from .my_redis import QueueRedis

red = QueueRedis()


def get_key(key):
	results = red.read_from_queue(key, 1)
	if results:
		result = results[0].decode().strip()
		# print(result)
		return result
	else:
		return 0
