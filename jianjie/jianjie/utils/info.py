import pymysql
from rediscluster import StrictRedisCluster

# redis
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

# etl
etl_conf = {'host': '172.31.215.38', 'port': 3306, 'user': 'base', 'password': 'imkloKuLiqNMc6Cn', 'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor}
etl = pymysql.connect(**etl_conf)
etl.select_db('spider')

online_conf = etl_conf.copy()
online_conf.update({'host': '172.31.215.33'})
online = pymysql.connect(**online_conf)
# online.select_db('spider')

kaifa_conf = etl_conf.copy()
kaifa_conf.update({'host': '172.31.215.36'})
kaifa = pymysql.connect(**kaifa_conf)
kaifa.select_db('innotree_data_assessment')

panshi_conf = etl_conf.copy()
panshi_conf.update({'host': '172.31.215.37'})
panshi = pymysql.connect(**panshi_conf)
# panshi.select_db('spider')

weisaite_conf = etl_conf.copy()
weisaite_conf.update({'host': '172.31.215.45'})
weisaite = pymysql.connect(**weisaite_conf)
# weisaite.select_db('spider')
