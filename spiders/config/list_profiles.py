# -*- coding: utf-8 -*-

# @File  : list_profiles.py
# @Author: zibang
# @Time  : 2月 24,2022
# @Desc  :


from settings import *
import requests
from loguru import logger


def list_all():
    """
    列出所有的配置文件
    :return:
    """
    params = {
        'token': VM_TOKEN,
    }
    url = f'{VM_URL}/profile/list'
    profiles_list = []
    result = requests.get(url, params)
    data_list = result.json().get('data')
    for data in data_list:
        sid = data.get('sid')
        profiles_list.append(sid)
    logger.debug('配置文件数量 : %s' % len(profiles_list))
    return profiles_list
