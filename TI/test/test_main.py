# !/usr/bin/env python
# -*- encoding: utf-8 -*-


from TI.test.proxy_pool import proxy_pool

if __name__ == '__main__':
    proxy = proxy_pool.get_proxy()  # 从IP池中提取IP
    print(proxy)
    if proxy:
        print(proxy)

        # parse_url(proxy)
