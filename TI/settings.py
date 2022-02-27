# -*- coding: utf-8 -*-

# @File  : settings.py
# @Author: zibang
# @Time  : 2月 10,2022
# @Desc  :


"""redis"""
# test
REDIS_TEST_HOST = 'r-wz95j265dca7ahyov7pd.redis.rds.aliyuncs.com'
REDIS_HOST = 'r-wz94l16plax2n2kusdpd.redis.rds.aliyuncs.com'
REDIS_PORT = 6379
REDIS_PASSWORD = 'lyt:GWZZPEQbvTKU1yZn2ZY7'
REDIS_TASK_KEY = 'ti_task:lyt'
REDIS_PROFILE_KEY = 'ti_task:profile'
REDIS_RESULT_KEY = 'ti_task:result'
REDIS_ERROR_KEY = 'ti_task:product_error'
REDIS_SUCCESS_KEY = 'ti_task:product_success'
REDIS_LOG_KEY = 'zibang:log'
REDIS_CHANNEL = 'task2'
REDIS_DB = 2

REDIS_PROXY_KEY = 'ti_task:proxy'

"""proxy"""
PROXY_COUNT = 35
PROXY_EX = 40

"""order"""
ORDER_ID = '954480323287312'

"""kdl"""
KDL_URL = 'http://dps.kdlapi.com/api/getdps/?orderid=954480323287312&num=1&signature=bfveudiqg9036cie2tzt9pt62gocv6pz&pt=1&f_loc=1&f_et=1&f_carrier=1&dedup=1&format=json&sep=1'

"""product url"""
PRODUCT_URL = 'https://www.ti.com.cn/store/ti/zh/p/product/?p=TIOL1123DRCR'
# PRODUCT_URL = 'https://www.ti.com.cn/product/cn/DLP3020-Q1?jktype=homepageproduct#order-quality'
