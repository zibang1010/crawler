# -*- coding: utf-8 -*-

# @File  : create_start_profile.py
# @Author: zibang
# @Time  : 2月 25,2022
# @Desc
from settings import *
# from redis import StrictRedis
import requests
import base64
import json


def create_start_profile():
    """
    /config/create_start
    :return:
    """

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    data = {
        # "proxyHost": "127.0.0.1",
        # "proxyPort": 1080,
        # "proxyUser": "username",
        # "proxyPass": "password",
        # "proxyType": "HTTP",  # HTTP/SOCKS4/SOCKS5/HTTPS
        "userAgent": "user_agent_value",
        "disablePlugins": True,
        "canvasDefType": "NOISEB",  # NOISEA | BLOCK | NOISEB | NOISEC | OFF
        "maskFonts": True,
        "platform": "platform_value",
        "langHdr": "en-US",
        "screenHeight": 900,
        "screenWidth": 1000,
        "timeZone": "Europe/Tallinn",
        "timeZoneFillOnStart": True,
        "startUrl": "https:#vmlogin.com/",
        "kernelVer": "90",
        "acceptLanguage": "en-US,en;q=0.9",
        "autoGeo_ip": False,
        "mobileEmulation": False,
        "deviceType": 1,
        "customdns": "8.8.8.8",
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
            "vendor": "vendor_value",
            "renderer": "renderer_value"
        },
        "webRtc": {
            "type": "FAKE",
            "fillOnStart": True,
            "publicIp": "6.6.6.6",
            "localIps": "192.168.1.100"
        }
    }
    encode = base64.b64encode(json.dumps(data).encode())
    print(encode)
    url = f'{VM_LOCAL_URL}/config/create_start'
    response = requests.post(url, data={'body': encode}, headers=headers)
    print(response.text)

if __name__ == '__main__':
    create_start_profile()
