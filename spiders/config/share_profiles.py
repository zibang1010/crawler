# -*- coding: utf-8 -*-

# @File  : share_profiles.py
# @Author: zibang
# @Time  : 2月 24,2022
# @Desc
from settings import VM_TOKEN, VM_URL
import requests


def share(profile):
    account_list = [
        'jxgl001@163.com',
        'jxgl002@163.com',
        'jxgl003@163.com',
        'jxgl004@163.com',
    ]
    for account in account_list:
        params = {
            "token": VM_TOKEN,
            "profileId": profile,
            "account": account
        }
        url = f'{VM_URL}/profile/share'
        result = requests.get(url, params=params)
        print(result.json())


if __name__ == '__main__':
    profile = 'EE167999-9805-43D6-A9BB-70B21979FF7B'
    share(profile)
