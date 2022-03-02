# -*- coding: utf-8 -*-

# @File  : collect_profiles.py
# @Author: zibang
# @Time  : 2月 28,2022
# @Desc
"""
    收集指纹
    1 获取在线所有的profiles列表
    2 遍历获取json文件 保存文本或发送到redis
"""
from config.list_profiles import list_all
from config.detail_profile import detail

def collect():
    profile_list = list_all()
    for profile in profile_list:
        data = detail(profile)
        del data['name']
        del data['proxyServer']
        print(data)

    print(len(profile_list))


if __name__ == '__main__':
    collect()
