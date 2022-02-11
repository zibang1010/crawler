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
REDIS_LOG_KEY = 'log:zibang'
REDIS_CHANNEL = 'task2'
REDIS_DB = 0
