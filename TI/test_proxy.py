# -*- coding: utf-8 -*-

# @File  : test_proxy.py
# @Author: zibang
# @Time  : 2月 09,2022
# @Desc  :  测试代理 proxy/text  控制 1~4s 优质
import requests
import time
from retrying import retry
from loguru import logger


def get_zm_proxy():
    url1 = 'http://http.tiqu.letecs.com/getip3?num=1&type=2&pro=0&city=0&yys=0&port=1&time=1&ts=1&ys=0&cs=1&lb=1&sb=0&pb=45&mr=1&regions=&username=chukou01&spec=1'
    url2 = 'http://http.tiqu.letecs.com/getip3?num=1&type=2&pro=0&city=0&yys=0&port=1&time=1&ts=1&ys=0&cs=1&lb=1&sb=0&pb=45&mr=1&regions=&gm=4&username=chukou01&spec=1'
    url3 = 'http://webapi.http.zhimacangku.com/getip?num=1&type=2&pro=0&city=0&yys=0&port=1&time=1&ts=1&ys=0&cs=1&lb=1&sb=0&pb=45&mr=1&regions=&username=chukou01&spec=1'

    resq = requests.get(url1)
    if resq.status_code == 200:
        data_json = resq.json()
        proxy_server = data_json.get('data')[0]
        return proxy_server
    else:
        print(resq.status_code)


def get_kdl_proxy():
    url = 'http://dps.kdlapi.com/api/getdps/?orderid=903248303961625&num=1&signature=v00i5zqu9gx14ylxc20dzmy1wbib2kkc&pt=1&sep=1'
    resq = requests.get(url)
    if resq.status_code == 200:
        text = resq.text
        ip, port = text.split(':')
        item = {
            'ip': ip,
            'port': port,
        }
        return item
    else:
        print(resq.status_code)


@retry
def test_proxy():
    # proxy_server = get_zm_proxy()
    proxy_server = get_kdl_proxy()
    # logger.debug(f"Get proxy_server：{proxy_server}")
    proxy_ip = proxy_server.get('ip')
    proxy_port = proxy_server.get('port')
    params = {
        'proxytype': 'http',
        'proxyserver': proxy_ip,
        'proxyport': proxy_port,
        'proxyusername': 'None',
        'proxypassword': 'None',
    }
    url = f'http://localhost:35000/api/v1/proxy/test?'
    try:
        resq = requests.get(url, params=params, timeout=5)
        if resq.status_code == 200:
            data = resq.json()
            status = data.get('status')
            value = data.get('value')
            if status == 'OK':
                # print('OK Value:\n', value)
                return proxy_server
            elif status == 'ERROR':
                logger.error(f'Error Value: {value}')
                return None
        else:
            logger.error(f'Error: local api err')
            return None
    except Exception as err:
        logger.warning("Proxy Timeout")
        raise


def on_proxy():
    start_time = time.time()
    proxy = test_proxy()
    if proxy:
        logger.debug(f"proxy_server：{proxy}")
        return proxy
    else:
        pass
    print('Time:', time.time() - start_time)
    time.sleep(2)


if __name__ == '__main__':
    on_proxy()
