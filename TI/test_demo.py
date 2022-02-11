# -*- coding: utf-8 -*-

# @File  : test_demo.py
# @Author: zibang
# @Time  : 2月 09,2022
# @Desc  :
import requests
from pprint import pprint
from db import RedisClient
from settings import *

redis = RedisClient(host=REDIS_TEST_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB)



def get_profile():
    token = '068ff736efe8c0b21bb6ece6980d68ae'
    base_url = f'https://api.vmlogin.com/v1/profile/list'
    params = {
        'token': token
    }
    resq = requests.get(base_url, params=params)
    print(resq.status_code)
    if resq.status_code == 200:
        data_json = resq.json()
        pprint(data_json)
        data_list = data_json.get('data')
        for data in data_list:
            profile = data.get('sid')
            print('profile:', profile)
            redis.radd(REDIS_PROFILE_KEY, profile)
    else:
        print(resq.status_code)


if __name__ == '__main__':
    get_profile()
