# -*- coding: utf-8 -*-

# @File  : detail_profile.py
# @Author: zibang
# @Time  : 2月 25,2022
# @Desc  :
from settings import *
import requests


def detail(profile):
    """
    /config/detail
    D66BE766-BE83-4A71-97EB-64F415C60DA3
    """
    params = {
        'token': VM_TOKEN,
        "profileId": profile,
        # 'tag': 'mac'
    }
    url = f'{VM_URL}/config/detail'
    result = requests.get(url, params)
    return result.json()


if __name__ == '__main__':
    profile = '0D521FE4-1A31-439E-BB5C-0677E52AC33B'
    print(detail(profile))