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
    profile = '03210349-4EE1-4F37-867C-54636E0BD71A'
    stop(profile)
