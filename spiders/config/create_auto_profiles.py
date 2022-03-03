# -*- coding: utf-8 -*-

# @File  : create_auto_profiles.py
# @Author: zibang
# @Time  : 2月 24,2022
# @Desc  :
import json

from config.browser_ua import random_ua
from random import choice
import random
import time
from pprint import pprint
from settings import *
import requests
from redis import StrictRedis
from loguru import logger

db = StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    db=6)

config = {
    "name": 'ahah',
    "userAgent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36",
    "uaCoreFollow": False,
    "canvasDefType": "NOISE",
    "maskFonts": True,
    "platform": "Win32",
    "langHdr": "es-AR",
    "screenHeight": 1050,
    "screenWidth": 1680,
    "timeZoneFillOnStart": False,
    "timeZone": "Asia/Shanghai",
    "startUrl": "about:blank",
    "kernelVer": "96",
    "audio": {
        "noise": True
    },
    "mediaDevices": {
        "setMediaDevices": True,
        "use_name": False,
        "list": {
            "videoInputs": [],
            "audioInputs": [],
            "audioOutputs": []
        },
        "videoInputs": 1,
        "audioInputs": 3,
        "audioOutputs": 0
    },
    "webgl": {
        "noise": True,
        "vendor": "Google Inc. (Intel)",
        "renderer": "ANGLE (NVIDIA GeForce MX150 Direct3D11 vs_5_0 ps_5_0)",
        "imgProtect": True
    },
    "webRtc": {
        "type": "FAKE",
        "fillOnStart": True,
        "wanSet": True,
        "lanSet": True,
        "publicIp": "224.162.109.180",
        "localIps": [
            "172.16.122.76"
        ]
    },
    "browserSettings": {
        "pepperFlash": False,
        "mediaStream": True,
        "webkitSpeech": True,
        "fakeUiForMedia": True,
        "gpuAndPepper3D": False,
        "ignoreCertErrors": False,
        "audioMute": False,
        "disableWebSecurity": False,
        "disablePdf": False,
        "touchEvents": False,
        "hyperlinkAuditing": True
    },
    "localCache": {
        "deleteCache": False,
        "deleteCookie": False,
        "clearCache": False,
        "clearHistory": False
    },
    "synSettings": {
        "synCookie": True,
        "synBookmark": True,
        "synHistory": True,
        "synExtension": False,
        "synKeepKey": True,
        "synLastTag": True
    },
    "leakProof": {
        "computerName": "PC-BJW2YZQG2I",
        "macAddress": "CC-F4-11-10-02-0C"
    },
    "browserParams": "",
    "customDns": "",
    "remoteDebug": {
        "bindAllDebug": False,
        "debuggingPort": 0,
        "logLevels": 99
    },
    "pluginFingerprint": {
        "pluginEnable": False,
        "list": {
            "name": [],
            "describe": [],
            "fileName": [],
            "mimeType": [],
            "mimeDescription": [],
            "mimeExtension": []
        }
    },
    "unPluginFingerprint": {
        "list": {
            "name": [],
            "describe": [],
            "fileName": [],
            "mimeType": [],
            "mimeDescription": [],
            "mimeExtension": []
        }
    },
    "browserApi": {
        "isCharging": True,
        "setBatteryStatus": False,
        "autoGeoIp": True,
        "setLatitude": False,
        "setLongitude": False,
        "setAccuracy": False,
        "setWebBluetooth": False,
        "setBluetoothAdapter": False,
        "speechSynthesis": False,
        "chargingTime": "0",
        "drainsTime": "Infinity",
        "batteryPercentage": "1",
        "latitude": "51.482594",
        "longitude": "-0.007661",
        "accuracy": "1803.34",
        "voiceURI": [],
        "name": [],
        "lang": [],
        "localService": [],
        "default": []
    },
    "sslFingerprint": {
        "enableCustomSSL": False,
        "versionMin": 0,
        "versionMax": 1,
        "cipherSuites": {
            "TLS_AES_128_GCM_SHA256": True,
            "TLS_AES_256_GCM_SHA384": True,
            "TLS_CHACHA20_POLY1305_SHA256": True,
            "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256": True,
            "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256": True,
            "TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384": True,
            "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384": True,
            "TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256": True,
            "TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256": True,
            "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA": True,
            "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA": True,
            "TLS_RSA_WITH_AES_128_GCM_SHA256": True,
            "TLS_RSA_WITH_AES_256_GCM_SHA384": True,
            "TLS_RSA_WITH_AES_128_CBC_SHA": True,
            "TLS_RSA_WITH_AES_256_CBC_SHA": True,
            "TLS_RSA_WITH_3DES_EDE_CBC_SHA": False,
            "TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA": False
        }
    },
    "otherProtection": {
        "setPortScan": True,
        "localPortsExclude": ""
    },
    "header": {
        "setHeaderCustom": False,
        "list": {
            "enable": [],
            "name": [],
            "value": [],
            "urlMatch": [],
            "notExistAdd": []
        }
    },
    "cmdcfg": {
        "openCommandLine": False,
        "commandLine": "",
        "closeCommandLine": True
    },
    "acceptLanguage": "es-AR,es;q=0.9",
    "hardwareConcurrency": 4,
    "dynamicFonts": True,
    "fontList": [],
    "clientRects": True,
    "fontSetting": {
        "dynamicFonts": True,
        "fontList": [],
        "clientRects": True
    },
    "doNotTrack": False,
    "hideWebdriver": False,
    "langBasedOnIp": True,
    "deviceMemory": 8,
    "product": "Gecko",
    "appName": "Netscape",
    "iconId": 0,
    "mobileEmulation": False,
    "deviceType": 0,
    "pixelRatio": "1.0",
    "os": "Windows"
}


def queue_count():
    """Queue Size"""
    size = db.llen(REDIS_PROFILE_KEY)
    return size


def get_ua():
    """
    随机获取UA /browsers/ua
    :return:
    """
    platform = 'windows'

    browser = 'chrome'
    params = {
        'token': VM_TOKEN,
        "platform": platform,
        "browser": browser
    }
    url = f'{VM_URL}/browsers/ua'
    result = requests.get(url, params)
    return result.json().get('data')


def create_profile():
    """
    随机创建配置
    :return:
    """
    data = get_ua()
    screen = data.get('screen')
    renderer = data.get('renderer')
    ua = data.get('ua')
    vendor = data.get('vendor')
    screenWidth, screenHeight = screen.split('x')
    config['name'] = time.strftime("%Y%m%d%H%M%S", time.localtime())
    webgl = config['webgl']
    webgl['renderer'] = renderer
    webgl['vendor'] = vendor
    config['userAgent'] = ua
    config['screenWidth'] = screenWidth
    config['screenHeight'] = screenHeight
    data = {
        "token": VM_TOKEN,
        "Body": json.dumps(config, ensure_ascii=False)
    }
    url = f'{VM_URL}/profile/create'
    result = requests.post(url, data=data)
    return result.json().get('value')


def share(profile):
    account_list = [
        'jxgl001@163.com',
        'jxgl002@163.com',
        'jxgl003@163.com',
        'jxgl004@163.com',
        'jxgl005@163.com',
    ]
    for account in account_list:
        params = {
            "token": VM_TOKEN,
            "profileId": profile,
            "account": account
        }
        url = f'{VM_URL}/profile/share'
        result = requests.get(url, params=params)
        data = result.json()
        value = data.get('value')
        print(value)
        status = data.get('status')
        if value == 218:
            logger.warning(f"{account}, {status}")
        elif value == 200:
            logger.debug(f"{account}, {status}")
        else:
            logger.error(f"Error： {result.json()}")



def start():
    """
    获取size
    创建指纹
    分享子账号
    push Queue
    :return:
    """
    # while 1:
    # print(create_profile())
    while 1:
        try:
            logger.debug('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            count = queue_count()
            if count < 450:
                logger.debug('Queue Count %s' % count)
                profile = create_profile()
                logger.debug('Profile: %s' % profile)
                share(profile)
                if db.lpush(REDIS_PROFILE_KEY, profile):
                    if db.zadd(REDIS_PROFILE_SCORE_KEY, {profile: 0}):
                        logger.debug('Add Queue Success: %s' % profile)
            else:
                logger.debug('=======================================')
                time.sleep(3)
        except Exception as err:
            logger.error(err)


if __name__ == '__main__':
    # print(random_browser())
    start()
