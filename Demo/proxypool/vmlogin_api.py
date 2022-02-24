# -*- coding: utf-8 -*-

# @File  : vmlogin_api.py
# @Author: zibang
# @Time  : 2月 13,2022
# @Desc
import requests
from loguru import logger
from db import RedisClient
from settings import *

# Base URL
base_url = 'https://api.vmlogin.com/v1'
token = '068ff736efe8c0b21bb6ece6980d68ae'


def on_request(method, url, params):
    if method == 'GET':
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Error: {response.status_code}")
            return None
    else:
        response = requests.post(url, json=params)
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Error: {response.status_code}")
            return None


# groups
def create_group(name):
    """
    创建一个组
    :return: {'status': 'OK', 'value': 191432}
    """
    params = {
        "token": token,
        "name": name
    }
    url = f'{base_url}/tag/create'
    method = 'GET'
    result = on_request(method, url, params)
    return result


def remove_group(name):
    """
    删除一个组
    :param name: 组名
    :return:
    """
    params = {
        "token": token,
        "tagId": name
    }
    url = f'{base_url}/tag/remove'
    method = 'GET'
    result = on_request(method, url, params)
    return result


def rename_group(old, new):
    """重命名一个组"""
    params = {
        "token": token,
        "name": new,
        "tagId": old,
    }
    method = 'GET'
    url = f'{base_url}/tag/rename'
    result = on_request(method, url, params)
    return result


def list_groups():
    """获取所有组的列表"""
    params = {
        "token": token
    }
    method = 'GET'
    url = f'{base_url}/tag/list'
    result = on_request(method, url, params)
    return result


def add_profile_group():
    """移动浏览器配置文件到特定的组"""
    pass


def remove_profile_group():
    """从特定组中删除浏览器配置文件"""
    pass


# profiles
def create_profile():
    data = {
        "token": token,
        "Body": {
            "name": "myProfile",
            "notes": "profile notes",
            "iconId": 0,
            "os": "Windows",
            "proxyServer": {
                "setProxyServer": True,
                "type": "HTTP",
                "host": "127.0.0.1",
                "port": "1080",
                "username": "hello",
                "password": "world"
            },
            "webRtc": {
                "type": "FAKE",
                "fillOnStart": True,
                "wanSet": True,
                "lanSet": True,
                "publicIp": "",
                "localIps": [
                    "192.168.1.10"
                ],
                "localIpsRand": False
            },
            "userAgent": "user_agent_value",
            "screenWidth": 1920,
            "screenHeight": 1080,
            "langHdr": "en-US",
            "acceptLanguage": "en-US,en;q=0.9",
            "platform": "platform_value",
            "product": "Gecko",
            "appName": "Netscape",
            "hardwareConcurrency": 4,
            "mobileEmulation": False,
            "deviceType": 1,
            "hideWebdriver": False,
            "langBasedOnIp": False,
            "doNotTrack": False,
            "deviceMemory": 8,
            "pixelRatio": "1.0",
            "maskFonts": True,
            "fontSetting": {
                "dynamicFonts": False,
                "fontList": [
                    "@Microsoft YaHei UI",
                    "@宋体",
                    "MS Outlook"
                ],
                "selectAll": False,
                "clientRects": True,
                "rand": False
            },
            "canvasDefType": "NOISEB",
            "audio": {
                "noise": True
            },
            "webgl": {
                "imgProtect": True,
                "vendor": "vendor_value",
                "renderer": "renderer_value"
            },
            "timeZoneFillOnStart": False,
            "timeZone": "Europe/Tallinn",
            "mediaDevices": {
                "setMediaDevices": True,
                "use_name": True,
                "videoInputs": 1,
                "audioInputs": 2,
                "audioOutputs": 4,
                "rand": {
                    "audioInputs": {
                        "device1": {
                            "label": "label value",
                            "deviceId": "deviceId value",
                            "groupId": "groupId value"
                        }
                    },
                    "audioOutputs": {
                        "device4": {
                            "label": "label value",
                            "deviceId": "deviceId value",
                            "groupId": "groupId value"
                        }
                    }
                }
            },
            "startUrl": "https://vmlogin.com/",
            "kernelVer": "90",
            "browserSettings": {
                "pepperFlash": True,
                "mediaStream": True,
                "webkitSpeech": True,
                "fakeUiForMedia": True,
                "gpuAndPepper3D": True,
                "ignoreCertErrors": True,
                "audioMute": True,
                "disableWebSecurity": True,
                "disablePdf": True,
                "touchEvents": True,
                "hyperlinkAuditing": True
            },
            "localCache": {
                "deleteCache": True,
                "deleteCookie": True,
                "clearCache": True,
                "clearHistory": True
            },
            "synSettings": {
                "synCookie": True,
                "synBookmark": True,
                "synHistory": True,
                "synExtension": True,
                "synKeepKey": True,
                "synLastTag": True
            },
            "leakProof": {
                "computerName": "",
                "macAddress": "",
                "rand": [
                    "computerName",
                    "macAddress"
                ]
            },
            "browserParams": "",
            "customDns": "",
            "remoteDebug": {
                "bindAllDebug": False,
                "debuggingPort": "",
                "logLevels": 99
            },
            "pluginFingerprint": {
                "pluginEnable": True,
                "list": {
                    "name": [
                        "Chrome PDF Plugin",
                        "Chrome PDF Viewer",
                        "Native Client",
                        "Shockwave Flash"
                    ],
                    "describe": [
                        "Portable Document Format",
                        "-",
                        "-",
                        "Shockwave Flash 32.0 r0"
                    ],
                    "fileName": [
                        "internal-pdf-viewer",
                        "mhjfbmdgcfjbbpaeojofohoefgiehjai",
                        "internal-nacl-plugin",
                        "pepflashplayer.dll"
                    ],
                    "mimeType": [
                        "application/x-google-chrome-pdf",
                        "application/pdf",
                        "application/x-nacl|application/x-pnacl",
                        "application/x-shockwave-flash|application/futuresplash"
                    ],
                    "mimeDescription": [
                        "Portable Document Format",
                        "-",
                        "Native Client Executable|-Portable Native Client Executable",
                        "Shockwave Flash|Shockwave Flash"
                    ],
                    "mimeExtension": [
                        "pdf",
                        "pdf",
                        "|",
                        "swf|spl"
                    ]
                }
            },
            "unPluginFingerprint": {
                "list": {
                    "name": [
                        "name"
                    ],
                    "describe": [
                        "describe"
                    ],
                    "fileName": [
                        "fileName"
                    ],
                    "mimeType": [
                        "mimeType"
                    ],
                    "mimeDescription": [
                        "mimeDescription"
                    ],
                    "mimeExtension": [
                        "mimeExtension"
                    ]
                }
            },
            "browserApi": {
                "setBatteryStatus": False,
                "isCharging": True,
                "chargingTime": "0",
                "drainsTime": "Infinity",
                "batteryPercentage": "1",
                "autoGeoIp": False,
                "setLatitude": False,
                "setLongitude": False,
                "setAccuracy": False,
                "latitude": "51.482594",
                "longitude": "-0.007661",
                "accuracy": "1803.34",
                "setWebBluetooth": False,
                "setBluetoothAdapter": False,
                "speechSynthesis": False,
                "speechVoicesList": {
                    "voiceURI": [
                        "voiceURI value 1",
                        "voiceURI value 2"
                    ],
                    "name": [
                        "name value 1",
                        "name value 2"
                    ],
                    "lang": [
                        "lang value 1",
                        "lang value 2"
                    ],
                    "localService": [
                        False,
                        True
                    ],
                    "default": [
                        True,
                        False
                    ]
                },
                "unSpeechVoicesList": {
                    "voiceURI": [
                        "voiceURI value 3"
                    ],
                    "name": [
                        "name value 3"
                    ],
                    "lang": [
                        "lang value 3"
                    ],
                    "localService": [
                        True
                    ],
                    "default": [
                        True
                    ]
                },
                "speechVoicesRestoreDefault": False
            },
            "sslFingerprint": {
                "enableCustomSSL": True,
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
                "localPortsExclude": "8000,12345,42069"
            },
            "header": {
                "setHeaderCustom": True,
                "list": {
                    "enable": [
                        False,
                        False,
                        True,
                        False
                    ],
                    "name": [
                        "name 1",
                        "name 2",
                        "name 3",
                        "name 4"
                    ],
                    "value": [
                        "value 1",
                        "value 2",
                        "value 3",
                        "value 4"
                    ],
                    "urlMatch": [
                        "urlMatch 1",
                        "urlMatch 2",
                        "urlMatch 3",
                        "urlMatch 4"
                    ],
                    "notExistAdd": [
                        True,
                        False,
                        False,
                        True
                    ]
                }
            },
            "cmdcfg": {
                "openCommandLine": False,
                "commandLine": "",
                "closeCommandLine": True
            },
            "tag": "group_name"
        }
    }
    method = 'POST'
    url = f'{base_url}/profile/create'
    result = on_request(method, url, data)
    return result


def update_profile():
    pass


def detail_profile():
    """
    获取浏览器配置文件详情
    :return:
    """
    params = {
        "token": token,
        "profileId": "289D9B08-AB9E-4606-931C-BF30BB875511"
    }
    method = 'GET'
    url = f'{base_url}/profile/detail'
    result = on_request(method, url, params)
    return result


def share_profile():
    pass


def cancel_share_profile():
    pass


def transfer_ownership():
    pass


def release_profile():
    """
    浏览器文件释放
    289D9B08-AB9E-4606-931C-BF30BB875511
    :return:
    """
    params = {
        "token": token,
        "profileId": "289D9B08-AB9E-4606-931C-BF30BB875511"
    }
    method = 'GET'
    url = f'{base_url}/profile/release)'
    result = on_request(method, url, params)
    return result


def list_profile():
    """
    获取浏览器配置文件的列表/profile/list
    :return: {'data': [{'sid': '289D9B08-AB9E-4606-931C-BF30BB875511', 'name': '1', 'tag': 'Default group', 'lastUsedTime': 0}], 'paging': {'totalCount': 1, 'currentPage': 1}}
    """
    params = {
        'token': token
    }
    url = f'{base_url}/profile/list'
    method = 'GET'
    result = on_request(method, url, params)
    return result


def random_browser_ua():
    """
    随机获取UA /browsers/ua
    :return:
    """
    params = {
        'token': token,
        "platform": "windows",
        "browser": "chrome"
    }
    url = f'{base_url}/browsers/ua'
    method = 'GET'
    result = on_request(method, url, params)
    return result


def run():
    db = RedisClient(
        host=REDIS_TEST_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        db=5)
    name = 'test'
    # result = create_group(name)
    result = list_profile()
    print(result)
    for data in result.get('data'):
        sid = data.get("sid")
        db.z(REDIS_PROFILE_KEY, sid)


if __name__ == '__main__':
    run()
