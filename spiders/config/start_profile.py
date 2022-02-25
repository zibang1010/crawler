# -*- coding: utf-8 -*-

# @File  : start_profile.py
# @Author: zibang
# @Time  : 2月 24,2022
# @Desc  :
import time

from settings import VM_LOCAL_URL, PROXY_USERNAME, PROXY_PASSWORD
import requests
from proxypool.random_proxy import get_proxy
from config.random_profile import get_profile


def start_profile():
    profile = get_profile()
    proxy = get_proxy()
    ip = proxy.get('ip')
    port = proxy.get('port')
    params = {
        "profileId": profile,
        "skiplock": True,
        "automation": True,
        "proxytype": "http",
        "proxyserver": ip,
        "proxyport": port,
        "proxyusername": PROXY_USERNAME,
        "proxypassword": PROXY_PASSWORD,
    }
    url = f'{VM_LOCAL_URL}/profile/start'
    result = requests.get(url, params=params)
    status = result.json().get('status')
    data = result.json()
    print(data)

    if status == 'ERROR':
        return None
    else:
        item = {
            'host': data.get('value'),
            'profileId': profile,
            'proxy': proxy
        }
        return item


if __name__ == '__main__':
    start_profile()
