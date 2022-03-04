# -*- coding: utf-8 -*-

# @File  : create_start_profiles.py
# @Author: zibang
# @Time  : 2月 24,2022
# @Desc  :
import time

import requests
from settings import VM_LOCAL_URL
import base64
import json
from proxypool.random_proxy import get_proxy
from settings import *
from config.stop_profile import stop_profile


config = {
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


def get_ua():
    """
    随机获取UA /browsers/ua
    并保存mongoDB备用
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


def create_local_profile():
    """
    初始化配置
    获取ua
    获取代理
    创建本地配置文件
    :return:
    """
    proxy = get_proxy()
    config['proxy'] = proxy
    ua = get_ua()
    # 添加proxy
    config['proxyPass'] = PROXY_PASSWORD
    config['proxyUser'] = PROXY_USERNAME
    config['proxyPort'] = int(proxy.get('port'))
    config['proxyHost'] = proxy.get('ip')
    config['proxyType'] = 'HTTP'
    config['startUrl'] = 'https://www.ip138.com/'

    # 获取UA
    data = get_ua()
    screen = data.get('screen')
    renderer = data.get('renderer')
    ua = data.get('ua')
    vendor = data.get('vendor')
    screenWidth, screenHeight = screen.split('x')
    # config['name'] = time.strftime("%Y%m%d%H%M%S", time.localtime())
    webgl = config['webgl']
    webgl['renderer'] = renderer
    webgl['vendor'] = vendor
    config['userAgent'] = ua
    config['screenWidth'] = screenWidth
    config['screenHeight'] = screenHeight

    return config

def create_start(data):
    proxy = data['proxy']
    del data['proxy']
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    encode = base64.b64encode(json.dumps(data).encode())
    url = f'{VM_LOCAL_URL}/profile/create_start'
    response = requests.post(url, data={'body': encode}, headers=headers)
    data = response.json()
    status = data.get('status')
    if status == 'ERROR':
        return None
    else:
        value = data.get('value')
        profileId = data.get('profileId')

        item = {
            'host': value,
            'profileId': profileId,
            'proxy': proxy
        }
        return item


def local_create():
    data = create_local_profile()
    result = create_start(data)
    return result


