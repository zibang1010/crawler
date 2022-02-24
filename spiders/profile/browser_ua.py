# -*- coding: utf-8 -*-

# @File  : browser_ua.py
# @Author: zibang
# @Time  : 2月 24,2022
# @Desc  :
import json
import time

from settings import VM_TOKEN, VM_URL
import requests
from pprint import pprint
from redis import StrictRedis
from settings import *

db = StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    db=6)


def random_ua(platform, browser):
    """
    随机获取UA /browsers/ua
    :return:
    """
    params = {
        'token': VM_TOKEN,
        "platform": platform,
        "browser": browser
    }
    url = f'{VM_URL}/browsers/ua'
    result = requests.get(url, params)
    return result.json().get('data')


if __name__ == '__main__':
    while 1:
        platform = 'windows'
        browser = 'chrome'
        data = random_ua(platform, browser)
        del data['screen']
        db.sadd(REDIS_UA_KEY, json.dumps(data,ensure_ascii=False))
        print(data)
        # time.sleep(1)
