# -*- coding: utf-8 -*-

# @File  : test_proxy.py
# @Author: zibang
# @Time  : 2月 12,2022
# @Desc
import json

import requests


def check_proxy():
    """
    测试代理
    :return:
    """
    proxy = '112.87.90.9:22277'
    proxies = {
        'http': 'http://' + proxy,
        'https': 'https://' + proxy,
    }
    try:
        response = requests.get('http://httpbin.org/get', proxies=proxies)
        print(response.text)
    except requests.exceptions.ConnectionError as e:
        print('Error', e.args)


def random_proxy():
    data = '{"msg": "", "code": 0, "data": {"count": 1, "proxy_list": ["113.218.236.25:19032,\u6e56\u5357\u7701\u5e38\u5fb7\u5e02,4307,571"], "order_left_count": 29541, "dedup_count": 1}}'
    data = json.loads(data)
    print(data)


if __name__ == '__main__':
    # random_proxy()
    check_proxy()