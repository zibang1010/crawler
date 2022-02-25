# -*- coding: utf-8 -*-

# @File  : create_c.py
# @Author: zibang
# @Time  : 2月 25,2022
# @Desc
from settings import *
# from redis import StrictRedis
import requests
#
# """
#    list:
#         list all config
#
#    delete:
#        删除配置文件在线服务
#        清空队列所有配置文件
#
#    create:
#        手动创建配置文件/自动化创建配置文件
#
#    share:
#        list 配置文件 批量共享所有用户
#
#    Push:
#        list 所有配置文件
#        push Redis Qeueu
#
#    """
#
# db = StrictRedis(
#     host=REDIS_TEST_HOST,
#     port=REDIS_PORT,
#     password=REDIS_PASSWORD,
#     db=5)


def list_all():
    params = {
        'token': VM_TOKEN,
    }
    url = f'{VM_URL}/profile/list'
    result = requests.get(url, params)
    print(result.json())
    return result.json()


# def delete():
#     pass
#
#
# def create():
#     pass
#
#
# def share():
#     pass
#
#
# def push():
#     pass
#
#
# def pull():
#     pass
#
#
# def start():
#     pass


if __name__ == '__main__':
    list_all()
