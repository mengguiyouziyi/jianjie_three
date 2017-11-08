import pymysql
from rediscluster import StrictRedisCluster

startup_nodes = [{"host": "172.29.237.209", "port": "7000"},
                 {"host": "172.29.237.209", "port": "7001"},
                 {"host": "172.29.237.209", "port": "7002"},
                 {"host": "172.29.237.214", "port": "7003"},
                 {"host": "172.29.237.214", "port": "7004"},
                 {"host": "172.29.237.214", "port": "7005"},
                 {"host": "172.29.237.215", "port": "7006"},
                 {"host": "172.29.237.215", "port": "7007"},
                 {"host": "172.29.237.215", "port": "7008"}]
rc = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)
etl_config = {'host': '172.31.215.38',
              'port': 3306,
              'user': 'spider',
              'password': 'spider',
              # 'db': 'dimension_result',
              'charset': 'utf8',
              'cursorclass': pymysql.cursors.DictCursor}
etl = pymysql.connect(**etl_config)
etl.select_db('dimension_result')
etl_cur = etl.cursor()
