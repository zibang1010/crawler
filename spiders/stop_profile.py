# -*- coding: utf-8 -*-

# @File  : stop_profile.py
# @Author: zibang
# @Time  : 2月 24,2022
# @Desc  :
from settings import VM_LOCAL_URL
import requests


def on_stop(profile):
    params = {
        "profileId": profile,
        "force": True
    }
    url = f'{VM_LOCAL_URL}/profile/stop'
    result = requests.get(url, params=params)
    print(result.text)


if __name__ == '__main__':
    profile = 'local_C4C792E6D3654B45845995C679A88773'
    on_stop(profile)
