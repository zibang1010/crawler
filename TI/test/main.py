# -*- coding: utf-8 -*-

# @File  : main.py
# @Author: zibang
# @Time  : 2月 14,2022
# @Desc  :
from TI.test.proxy_pool import ProxyPool

if __name__ == '__main__':
    pool = ProxyPool(4)
    print(pool.get_proxy())
