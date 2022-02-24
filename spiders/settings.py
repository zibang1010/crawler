# -*- coding: utf-8 -*-

# @File  : settings.py
# @Author: zibang
# @Time  : 2月 24,2022
# @Desc  :

from environs import Env

"""
获取代理
获取资源
代理减分/加分
资源减分/加分
推送log
更改TI料配置
"""
env = Env()

"""redis"""
REDIS_HOST = env.str("REDIS_HOST", 'r-wz94l16plax2n2kusdpd.redis.rds.aliyuncs.com')
REDIS_TEST_HOST = env.str("REDIS_TEST_HOST", 'r-wz95j265dca7ahyov7pd.redis.rds.aliyuncs.com')
REDIS_PORT = env.int("REDIS_PORT", 6379)
REDIS_PASSWORD = env.str("REDIS_PASSWORD", 'lyt:GWZZPEQbvTKU1yZn2ZY7')
REDIS_TASK_KEY = 'ti_task:task'
REDIS_PROFILE_KEY = 'ti_task:profile'
REDIS_UA_KEY = 'ti_task:ua'
REDIS_COUNT_LOG_KEY = 'lyt:ti_log'
REDIS_PROXY_KEY = 'ti_task:proxy'
REDIS_CHANNEL = 'task2'
REDIS_DB = 6

"""proxy"""
PROXY_COUNT = 35
PROXY_EX = 40

"""order"""
ORDER_ID = '954480323287312'

"""kdl"""
KDL_URL = 'http://dps.kdlapi.com/api/getdps/?orderid=954480323287312&num=1&signature=bfveudiqg9036cie2tzt9pt62gocv6pz&pt=1&f_loc=1&f_et=1&f_carrier=1&dedup=1&format=json&sep=1'

"""product url"""
PRODUCT_URL = 'https://www.ti.com/store/ti/zh/p/product/?p=LMK1D1208IRHAR'

"""ES_HOST"""
ES_HOST = env.str("ES_HOST", 'http://127.0.0.1:9200/')

"""VMLogin"""
VM_URL = env.str("VM_URL", 'https://api.vmlogin.com/v1')
VM_TOKEN = env.str("VM_TOKEN", '068ff736efe8c0b21bb6ece6980d68ae')
VM_LOCAL_URL = env.str("VM_LOCAL_URL", 'http://192.168.1.126:35000/api/v1')
