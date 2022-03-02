# -*- coding: utf-8 -*-

# @File  : create_start_profiles.py
# @Author: zibang
# @Time  : 2月 24,2022
# @Desc  :
import time

import requests
from settings import VM_LOCAL_URL
import base64
import json
from proxypool.random_proxy import get_proxy
from settings import *
from config.stop_profile import stop_profile


def read_config():
    # 获取代理
    proxy = get_proxy()
    print(proxy)
    with open('./score/A8010BAB-6E04-4273-A4AD-18F3A87890F9.json', 'r') as f:
        result = f.read()
        data = json.loads(result)
        """
          "name": "500(119)",
          "proxyPass": "",
          "proxyUser": "",
          "proxyPort": "",
          "proxyHost": "",
          "proxyType": "HTTP",
        """
        del data['name']
        del data['proxyServer']
        data['proxyPass'] = PROXY_PASSWORD
        data['proxyUser'] = PROXY_USERNAME
        data['proxyPort'] = proxy.get('port')
        data['proxyHost'] = proxy.get('ip')
        data['proxyType'] = 'HTTP'
        data['startUrl'] = 'https://www.ip138.com/'
        return data


def create_start(data):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    encode = base64.b64encode(json.dumps(data).encode())
    url = f'{VM_LOCAL_URL}/profile/create_start'
    response = requests.post(url, data={'body': encode}, headers=headers)
    data = response.json()
    status = data.get('status')
    if status == 'ERROR':
        return None
    else:
        value = data.get('value')
        profileId = data.get('profileId')

        item = {
            'host': value,
            'profileId': profileId,
            'proxy': proxy
        }
        return item


def star():
    data = read_config()
    result = create_start(data)
    profileId = result.get('profileId')
    value = result.get('value')
    time.sleep(10)
    stop_profile(profileId)


if __name__ == '__main__':
    star()
