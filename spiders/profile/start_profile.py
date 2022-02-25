# -*- coding: utf-8 -*-

# @File  : start_profile.py
# @Author: zibang
# @Time  : 2月 24,2022
# @Desc  :
from settings import VM_LOCAL_URL, PROXY_USERNAME, PROXY_PASSWORD
import requests
from proxypool.random import get_proxy


def start_profile(profile, proxy):
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
    print(result.json())
    if status == 'ERROR':
        pass
    else:
        pass


def run():
    proxy = get_proxy()
    profile = '03210349-4EE1-4F37-867C-54636E0BD71A'
    start_profile(profile, proxy)


if __name__ == '__main__':
    pass
