# -*- coding: utf-8 -*-

# @File  : detail_profile.py
# @Author: zibang
# @Time  : 2月 25,2022
# @Desc  :

from pprint import pprint
from redis import StrictRedis
from settings import *
import requests
from loguru import logger
from save_profile import save

db = StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    db=6)


def get_profile():
    """
    获取分数高的指纹
    保存到文本
    :return:
    """
    profile_list = []
    result = db.zrangebyscore(REDIS_PROFILE_SCORE_KEY, 4, 100)
    for profile in result:
        profile_list.append(str(profile, encoding='utf-8'))

    print("profile_list: ", len(profile_list))
    return profile_list


def detail(profile):
    """
    /config/detail
    D66BE766-BE83-4A71-97EB-64F415C60DA3
    """
    params = {
        'token': VM_TOKEN,
        "profileId": profile,
    }
    url = f'{VM_URL}/profile/detail'
    result = requests.get(url, params)
    return result.json()


if __name__ == '__main__':
    # profile = '0CBCFEBF-07F1-4340-9CE4-86CCE441A9DB'
    # pprint(detail(profile))
    profile_list = get_profile()
    for profile in profile_list:
        data = detail(profile)
        save(profile, data)
