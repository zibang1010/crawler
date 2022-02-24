# -*- coding: utf-8 -*-

# @File  : random_profile.py
# @Author: zibang
# @Time  : 2月 24,2022
# @Desc  :
from settings import VM_LOCAL_URL
import requests


def random():
    params = {
        "platform": "Windows",
        "langHdr": "en-US",
        "acceptLanguage": "en-US,en;q=0.9",
        "timeZone": "America/New_York"
    }
    url = f'{VM_LOCAL_URL}/profile/randomProfile'
    result = requests.get(url, params=params)
    print(result.text)


if __name__ == '__main__':
    random()
