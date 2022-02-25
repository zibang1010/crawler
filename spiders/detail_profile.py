# -*- coding: utf-8 -*-

# @File  : detail_profile.py
# @Author: zibang
# @Time  : 2月 25,2022
# @Desc  :
from settings import *
import requests
from pprint import pprint

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
    profile = 'D66BE766-BE83-4A71-97EB-64F415C60DA3'
    pprint(detail(profile))