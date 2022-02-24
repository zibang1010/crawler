# -*- coding: utf-8 -*-

# @File  : test_api.py
# @Author: zibang
# @Time  : 2月 16,2022
# @Desc  :
import requests
from settings import *


def request_api(flag, key=None):
    if flag == 'add':
        url = f'http://{API_HOST}:{API_PORT}/api/v1/add'
    elif flag == 'remove':
        url = f'http://{API_HOST}:{API_PORT}/api/v1/remove'
    else:
        url = f'http://{API_HOST}:{API_PORT}/api/v1/random'

    params = {'key': key}
    try:
        response = requests.get(url, json=params)
        if response.status_code == 200:
            print(response.text)
            return True
        else:
            print(response.status_code)
            return None
    except Exception as err:
        print('err:', err)
        return None


if __name__ == '__main__':
    result = request_api(flag='random')
    print(result)
