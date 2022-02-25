# -*- coding: utf-8 -*-

# @File  : release_profile.py
# @Author: zibang
# @Time  : 2月 24,2022
# @Desc  :
import requests
from settings import *


def release(profile):
    params = {
        "token": VM_TOKEN,
        "profileId": profile
    }
    url = f'{VM_URL}/profile/release'
    print(url)
    result = requests.get(url, params=params)
    print(result.text)


if __name__ == '__main__':
    profile = 'B931DD89-DBC5-44EC-9667-80C19008DD98'
    release(profile)
