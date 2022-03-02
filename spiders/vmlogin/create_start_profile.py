# -*- coding: utf-8 -*-

# @File  : create_start_profiles.py
# @Author: zibang
# @Time  : 2月 25,2022
# @Desc
from settings import *
from redis import StrictRedis
import requests
import base64
import json
from pprint import pprint
from loguru import logger
import time

db = StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    db=6)


def on_stop(profile):
    params = {
        "profileId": profile,
        "force": True
    }
    url = f'{VM_LOCAL_URL}/config/stop'
    result = requests.get(url, params=params)
    print(result.text)


def get_proxy():
    return {
        "host": "36.6.148.13:18223",
        "ip": "36.6.148.13",
        "port": "18223",
        "address": "安徽省淮北市",
        "expire": "1794",
        "operator": "电信",
        "md5": "74a5ced6869f5ecbb9b8695fe62ee43f"
    }


def get_ua():
    result = db.srandmember('ti_task:ua')
    data = json.loads(result)
    pprint(data)
    return data


def on_start():
    """
    /config/create_start
    :return:
    """
    s_t = time.time()
    proxy = get_proxy()
    config = get_ua()
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "proxyHost": proxy.get('ip'),
        "proxyPort": proxy.get('port'),
        "proxyUser": PROXY_USERNAME,
        "proxyPass": PROXY_PASSWORD,
        "proxyType": "HTTP",  # HTTP/SOCKS4/SOCKS5/HTTPS
        "userAgent": config.get('ua'),
        "disablePlugins": True,
        "canvasDefType": "NOISE",  # NOISEA | BLOCK | NOISEB | NOISEC | OFF
        "maskFonts": True,
        "platform": "Windows",
        "langHdr": 'zh-CN',
        "screenHeight": 1152,
        "screenWidth": 2048,
        "timeZone": "Europe/Tallinn",
        "timeZoneFillOnStart": True,
        "startUrl": "https://www.ip138.com/",
        # "startUrl": "https://www.ti.com.cn",
        "kernelVer": "96",
        "acceptLanguage": "zh-CN,zh;q=0.9",
        "autoGeo_ip": True,
        "mobileEmulation": False,
        "deviceType": 0,
        "customdns": "",
        "audio": {
            "noise": True
        },
        "mediaDevices": {
            "audioInputs": 3,
            "audioOutputs": 2,
            "videoInputs": 1
        },
        "webgl": {
            "noise": True,
            "vendor": config.get('vendor'),
            "renderer": config.get('renderer')
        },
        "webRtc": {
            "type": "FAKE",
            "fillOnStart": True,
            "publicIp": "57.191.200.171",
            "localIps": "192.168.1.100"
        }
    }
    encode = base64.b64encode(json.dumps(data).encode())
    url = f'{VM_LOCAL_URL}/config/create_start'
    response = requests.post(url, data={'body': encode}, headers=headers)
    data = response.json()
    status = data.get('status')
    if status == 'OK':
        profileId = data.get('profileId')
        item = {
            'host': data.get('value'),
            'profileId': profileId,
        }
        logger.debug(item)
        return item
        # time.sleep(10)
        # stop(profileId)
    else:
        print(data)
        return None

    # e_t = time.time()
    # print('time:', e_t - s_t)

# if __name__ == '__main__':
#     while True:
#         start()
