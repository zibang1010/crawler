# -*- coding: utf-8 -*-

# @File  : demo2.py
# @Author: zibang
# @Time  : 2月 06,2022
# @Desc
import requests



data = {
    "profileId": "D:/app/VMLogin/profile/0C1D5965-4933-4C76-AE73-3EC7FE47532A",
    "url": "www.vmlogin.com"}
task = '/profile/openurl'
req = requests.get(f'http://127.0.0.1:35000/api/v1{task}', params=data)
print('Status:', req.status_code)
print(req.text)