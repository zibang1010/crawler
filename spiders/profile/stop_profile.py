# -*- coding: utf-8 -*-

# @File  : stop_profile.py
# @Author: zibang
# @Time  : 2月 24,2022
# @Desc  :
from settings import VM_LOCAL_URL
import requests


def stop(profile):
    params = {
        "profileId": profile,
        "force": True
    }
    url = f'{VM_LOCAL_URL}/profile/stop'
    result = requests.get(url, params=params)
    print(result.text)


if __name__ == '__main__':
    profile = 'B931DD89-DBC5-44EC-9667-80C19008DD98'
    stop(profile)
