# -*- coding: utf-8 -*-

# @File  : demo.py
# @Author: zibang
# @Time  : 2月 17,2022
# @Desc  :

import requests
from pprint import pprint


# /profile/detail
def detail(name):
    """浏览器配置文件详情"""
    params = {
        "token": '068ff736efe8c0b21bb6ece6980d68ae',
        "profileId": name
    }
    url = 'https://api.vmlogin.com/v1/profile/detail'
    result = requests.get(url, params)
    data = result.json()
    print(data)
    status = data.get('status')
    if status == "ERROR":
        return None
    else:
        return data


def release(name):
    """释放文件"""
    params = {
        "token": '068ff736efe8c0b21bb6ece6980d68ae',
        "profileId": name
    }
    url = 'https://api.vmlogin.com/v1/profile/release'
    result = requests.get(url, params)
    data = result.json()
    status = data.get('status')
    if status == "ERROR":
        return None
    else:
        return True


def remove(name):
    """
    移除profile
    :return: {'status': 'OK', 'value': 191432}
    """
    params = {
        "token": '068ff736efe8c0b21bb6ece6980d68ae',
        "profileId": name
    }
    url = 'https://api.vmlogin.com/v1/profile/remove'
    result = requests.get(url, params)
    data = result.json()
    print(data)
    status = data.get('status')
    if status == "ERROR":
        return None
    else:
        return True


# print(remove_profile('25E90471-27F6-4B63-BE51-DE83A1D3EDA8'))
# print(release_profile('25E90471-27F6-4B63-BE51-DE83A1D3EDA8'))
# print(active_profile('25E90471-27F6-4B63-BE51-DE83A1D3EDA8'))
pprint(detail('54A9584D-33D2-4818-A741-E9CF351A73F9'))
