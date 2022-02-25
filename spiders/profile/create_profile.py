# -*- coding: utf-8 -*-

# @File  : create_profile.py
# @Author: zibang
# @Time  : 2月 24,2022
# @Desc  :
import json

from profile.browser_ua import random_ua
from random import choice
import random
import time
from pprint import pprint
from settings import *
import requests


def create_profile():
    """
    随机创建指纹
    :return:
    """
    body = create_config()
    data = {
        "token": VM_TOKEN,
        "Body": json.dumps(body, ensure_ascii=False)
    }

    url = f'{VM_URL}/profile/create'
    result = requests.post(url, data=data)
    print(result.text)
    return result.json().get('value')


def create_config():
    """
    随机创建配置
    :return:
    """
    platform = 'windows'
    browser = 'chrome'
    data = random_ua(platform, browser)
    screen = data.get('screen')
    renderer = data.get('renderer')
    ua = data.get('ua')
    vendor = data.get('vendor')
    screenWidth, screenHeight = screen.split('x')
    screenWidth = 1920
    screenHeight = 1080
    hardwareConcurrency = [8, 16, 12, 4, 32]  # 1~64
    deviceMemory = [8]
    fontList = [
        "@Fixedsys",
        "@Malgun Gothic",
        "@Malgun Gothic Semilight",
        "@Microsoft JhengHei",
        "@Microsoft JhengHei Light",
        "@Microsoft JhengHei UI",
        "@Microsoft JhengHei UI Light",
        "@Microsoft YaHei UI",
        "@Microsoft YaHei UI Light",
        "@MingLiU_HKSCS-ExtB",
        "@MingLiU-ExtB",
        "@MS Gothic",
        "@MS PGothic",
        "@MS UI Gothic",
        "@PMingLiU-ExtB",
        "@SimSun-ExtB",
        "@System",
        "@Terminal",
        "@Yu Gothic",
        "@Yu Gothic Light",
        "@Yu Gothic Medium",
        "@Yu Gothic UI",
        "@Yu Gothic UI Light",
        "@Yu Gothic UI Semibold",
        "@Yu Gothic UI Semilight",
        "@等线",
        "@等线 Light",
        "@方正舒体",
        "@方正姚体",
        "@仿宋",
        "@黑体",
        "@华文彩云",
        "@华文仿宋",
        "@华文行楷",
        "@华文琥珀",
        "@华文楷体",
        "@华文隶书",
        "@华文宋体",
        "@华文细黑",
        "@华文新魏",
        "@华文中宋",
        "@楷体",
        "@隶书",
        "@宋体",
        "@微软雅黑",
        "@微软雅黑 Light",
        "@新宋体",
        "@幼圆",
        "Agency FB",
        "Algerian",
        "Arial",
        "Arial Black",
        "Arial Narrow",
        "Arial Rounded MT Bold",
        "Bahnschrift",
        "Bahnschrift Condensed",
        "Bahnschrift Light",
        "Bahnschrift Light Condensed",
        "Bahnschrift Light SemiCondensed",
        "Bahnschrift SemiBold",
        "Bahnschrift SemiBold Condensed",
        "Bahnschrift SemiBold SemiConden",
        "Bahnschrift SemiCondensed",
        "Bahnschrift SemiLight",
        "Bahnschrift SemiLight Condensed",
        "Bahnschrift SemiLight SemiConde",
        "Baskerville Old Face",
        "Bauhaus ",
        "Bell MT",
        "Berlin Sans FB",
        "Berlin Sans FB Demi",
        "Bernard MT Condensed",
        "Blackadder ITC",
        "Bodoni MT",
        "Bodoni MT Black",
        "Bodoni MT Condensed",
        "Bodoni MT Poster Compressed",
        "Book Antiqua",
        "Bookman Old Style",
        "Bookshelf Symbol ",
        "Bradley Hand ITC",
        "Britannic Bold",
        "Broadway",
        "Brush Script MT",
        "Calibri",
        "Calibri Light",
        "Californian FB",
        "Calisto MT",
        "Cambria",
        "Cambria Math",
        "Candara",
        "Candara Light",
        "Castellar",
        "Centaur",
        "Century",
        "Century Gothic",
        "Century Schoolbook",
        "Chiller",
        "Colonna MT",
        "Comic Sans MS",
        "Consolas",
        "Constantia",
        "Cooper Black",
        "Copperplate Gothic Bold",
        "Copperplate Gothic Light",
        "Corbel",
        "Corbel Light",
        "Courier",
        "Courier New",
        "Curlz MT",
        "Default",
        "DejaVu Sans Mono",
        "Dubai",
        "Dubai Light",
        "Dubai Medium",
        "Ebrima",
        "Edwardian Script ITC",
        "Elephant",
        "Engravers MT",
        "Eras Bold ITC",
        "Eras Demi ITC",
        "Eras Light ITC",
        "Eras Medium ITC",
        "Felix Titling",
        "Fixedsys",
        "Footlight MT Light",
        "Forte",
        "Franklin Gothic Book",
        "Franklin Gothic Demi",
        "Franklin Gothic Demi Cond",
        "Franklin Gothic Heavy",
        "Franklin Gothic Medium",
        "Franklin Gothic Medium Cond",
        "Freestyle Script",
        "French Script MT",
        "Gabriola",
        "Gadugi",
        "Garamond",
        "Georgia",
        "Gigi",
        "Gill Sans MT",
        "Gill Sans MT Condensed",
        "Gill Sans MT Ext Condensed Bold",
        "Gill Sans Ultra Bold",
        "Gill Sans Ultra Bold Condensed",
        "Gloucester MT Extra Condensed",
        "Goudy Old Style",
        "Goudy Stout",
        "Haettenschweiler",
        "Harlow Solid Italic",
        "Harrington",
        "High Tower Text",
        "HoloLens MDL Assets",
        "HP Simplified",
        "HP Simplified Light",
        "Impact",
        "Imprint MT Shadow",
        "Informal Roman",
        "Ink Free",
        "Javanese Text",
        "jdFontAwesome",
        "jdFontCustom",
        "jdIcoFont",
        "jdIcoMoonFree",
        "jdiconfontA",
        "jdiconfontB",
        "jdiconfontC",
        "jdiconfontD",
        "JdIonicons",
        "Jokerman",
        "Juice ITC",
        "Kristen ITC",
        "Kunstler Script",
        "Leelawadee UI",
        "Leelawadee UI Semilight",
        "Lucida Bright",
        "Lucida Calligraphy",
        "Lucida Console",
        "Lucida Fax",
        "Lucida Handwriting",
        "Lucida Sans",
        "Lucida Sans Typewriter",
        "Lucida Sans Unicode",
        "Magneto",
        "Maiandra GD",
        "Malgun Gothic",
        "Malgun Gothic Semilight",
        "Marlett",
        "Matura MT Script Capitals",
        "Microsoft Himalaya",
        "Microsoft JhengHei",
        "Microsoft JhengHei Light",
        "Microsoft JhengHei UI",
        "Microsoft JhengHei UI Light",
        "Microsoft New Tai Lue",
        "Microsoft PhagsPa",
        "Microsoft Sans Serif",
        "Microsoft Tai Le",
        "Microsoft YaHei UI",
        "Microsoft YaHei UI Light",
        "Microsoft Yi Baiti",
        "MingLiU_HKSCS-ExtB",
        "MingLiU-ExtB",
        "Mistral",
        "Modern",
        "Modern No. ",
        "Monaco",
        "Mongolian Baiti",
        "Monotype Corsiva",
        "MS Gothic",
        "MS Outlook",
        "MS PGothic",
        "MS Reference Sans Serif",
        "MS Reference Specialty",
        "MS Sans Serif",
        "MS Serif",
        "MS UI Gothic",
        "MT Extra",
        "MV Boli",
        "Myanmar Text",
        "Niagara Engraved",
        "Niagara Solid",
        "Nirmala UI",
        "Nirmala UI Semilight",
        "OCR A Extended",
        "Old English Text MT",
        "Onyx",
        "Palace Script MT",
        "Palatino Linotype",
        "Papyrus",
        "Parchment",
        "Perpetua",
        "Perpetua Titling MT",
        "Playbill",
        "PMingLiU-ExtB",
        "Poor Richard",
        "Pristina",
        "Rage Italic",
        "Ravie",
        "Rockwell",
        "Rockwell Condensed",
        "Rockwell Extra Bold",
        "Roman",
        "Script",
        "Script MT Bold",
        "Segoe MDL Assets",
        "Segoe Print",
        "Segoe Script",
        "Segoe UI",
        "Segoe UI Black",
        "Segoe UI Emoji",
        "Segoe UI Historic",
        "Segoe UI Light",
        "Segoe UI Semibold",
        "Segoe UI Semilight",
        "Segoe UI Symbol",
        "Showcard Gothic",
        "SimSun-ExtB",
        "Sitka Banner",
        "Sitka Display",
        "Sitka Heading",
        "Sitka Small",
        "Sitka Subheading",
        "Sitka Text",
        "Small Fonts",
        "Snap ITC",
        "Stencil",
        "Sylfaen",
        "Symbol",
        "System",
        "Tahoma",
        "Tempus Sans ITC",
        "Terminal",
        "Times New Roman",
        "Trebuchet MS",
        "Tw Cen MT",
        "Tw Cen MT Condensed",
        "Tw Cen MT Condensed Extra Bold",
        "Verdana",
        "Viner Hand ITC",
        "Vivaldi",
        "Vladimir Script",
        "Webdings",
        "Wide Latin",
        "Wingdings",
        "Wingdings ",
        "Wingdings ",
        "Yu Gothic",
        "Yu Gothic Light",
        "Yu Gothic Medium",
        "Yu Gothic UI",
        "Yu Gothic UI Light",
        "Yu Gothic UI Semibold",
        "Yu Gothic UI Semilight",
        "等线",
        "等线 Light",
        "方正舒体",
        "方正姚体",
        "仿宋",
        "黑体",
        "华文彩云",
        "华文仿宋",
        "华文行楷",
        "华文琥珀",
        "华文楷体",
        "华文隶书",
        "华文宋体",
        "华文细黑",
        "华文新魏",
        "华文中宋",
        "楷体",
        "隶书",
        "宋体",
        "微软雅黑",
        "微软雅黑 Light",
        "新宋体",
        "幼圆"
    ]
    fontList = random.sample(fontList, random.randint(3, 30))
    cts = time.strftime("%Y%m%d%H%M%S", time.localtime())
    config = {
        "name": f"{cts}",  # 基础设置 -> 显示名称
        "notes": "",  # 基础设置 -> 备注信息
        "iconId": 1,  # 基础设置 -> ICON 图标 0 ~ 30
        "os": "Windows",  # 基础设置 -> 操作系统
        "proxyServer": {
            "setProxyServer": False,  # 基础设置 -> 设置代理服务器 -> 启用代理服务器
            "type": "HTTP",  # 基础设置 -> 设置代理服务器 -> 代理类型（HTTP、SOCKS4、SOCKS5、HTTPS）
            "host": "127.0.0.1",  # 基础设置 -> 设置代理服务器 -> IP地址
            "port": "1080",  # 基础设置 -> 设置代理服务器 -> 端口
            "username": "hello",  # 基础设置 -> 设置代理服务器 -> 登录用户
            "password": "world"  # 基础设置 -> 设置代理服务器 -> 登录密码
        },
        "webRtc": {
            "type": "FAKE",
            # 基础设置 -> WebRtc  OFF:【真实模式】启用webrtc插件  BLOCK:【禁用模式A】禁用webrtc插件  FAKE:【替换模式】返回指定的IP地址  BLOCKB:【禁用模式B】禁用webrtc插件(全面)
            "fillOnStart": True,  # 基础设置 -> 自动检测IP
            "wanSet": True,  # Basic setup -> 公网IP设置开关
            "lanSet": True,  # Basic setup -> 内网IP设置开关
            "publicIp": "5.5.5.5",  # 基础设置 -> 公网IP
            "localIps": [
                "192.168.1.10"  # 基础设置 -> 内网IP
            ],
            "localIpsRand": True  # 基础设置 -> 内网IP 随机
        },
        "userAgent": f"{ua}",  # Navigator参数 -> User-Agent
        "screenWidth": int(screenWidth),  # Navigator参数 -> 分辨率宽度
        "screenHeight": int(screenHeight),  # Navigator参数 -> 分辨率高度
        "langHdr": "en-US",  # Navigator参数 -> 语言
        "acceptLanguage": "en-US,en;q=0.9",  # Navigator参数 -> Accept-Language
        "platform": f"{platform}",  # Navigator参数 -> Platform
        "product": "Gecko",  # Navigator参数 -> Product
        "appName": "Netscape",  # Navigator参数 -> appName
        "hardwareConcurrency": choice(hardwareConcurrency),  # Navigator参数 -> hardwareConcurrency(1 ~ 64)
        "mobileEmulation": False,  # Navigator参数 -> 移动仿真
        "deviceType": 1,  # Navigator参数 -> 移动仿真类型  0: Desktop  1: Mobile
        "hideWebdriver": False,  # Navigator参数 -> hideWebdriver
        "langBasedOnIp": True,  # Navigator参数 -> 基于IP设置语言
        "doNotTrack": False,  # Navigator参数 -> 请勿追踪
        "deviceMemory": choice(deviceMemory),  # Navigator参数 -> deviceMemory
        "pixelRatio": "1.0",  # Navigator参数 -> Device pixel Ratio
        "maskFonts": True,  # 高级指纹保护设置 -> 启用【字体】指纹保护
        "fontSetting": {
            "dynamicFonts": False,  # 高级指纹保护设置 -> 设置字体 -> 不使用字体列表，每次动态随机（False：使用 True：不使用）
            "fontList": fontList,
            "selectAll": False,  # 高级指纹保护设置 -> 设置字体 -> 全选
            "clientRects": True,  # 高级指纹保护设置 -> 设置字体 -> ClientRects指纹增强保护
            "rand": False  # 高级指纹保护设置 -> 设置字体 -> 随机字体
        },
        "canvasDefType": "NOISEB",
        # 高级指纹保护设置 -> 【Canvas】保护（类型）:噪声模式A(NOISEA) | 封锁模式(BLOCK) | 噪声模式B(NOISEB) | 噪声模式C(NOISEC) | 不启用(OFF)
        "audio": {
            "noise": True  # 高级指纹保护设置 -> 启用硬件指纹【AudioContext】保护（噪声模式）
        },
        "webgl": {
            "imgProtect": True,  # 高级指纹保护设置 -> 【WebGL】图像保护
            "vendor": f"{vendor}",  # 高级指纹保护设置 -> 启用硬件指纹【WebGL】保护 -> WebGL vendor
            "renderer": f"{renderer}"  # 高级指纹保护设置 -> 启用硬件指纹【WebGL】保护 -> WebGL renderer
        },
        "timeZoneFillOnStart": True,  # 高级指纹保护设置 -> 启用基于IP设置时区
        "timeZone": "Europe/Tallinn",  # 高级指纹保护设置 -> 手工指定时区
        "mediaDevices": {  # 媒体设备指纹设置
            "setMediaDevices": True,  # 媒体设备指纹设置 -> 自定义媒体设备数量
            "use_name": False,  # 媒体设备指纹设置 -> 指定设备名称
            "videoInputs": 1,  # 媒体设备指纹设置 -> 视频输入（取值范围 0 ~ 1）
            "audioInputs": 2,  # 媒体设备指纹设置 -> 音频输入（取值范围 0 ~ 4）
            "audioOutputs": 4,  # 媒体设备指纹设置 -> 音频输出（取值范围 0 ~ 4）
            # /*
            # | -------------------------------------------------------------------
            # |  对所有的 或者 指定的媒体设备信息进行更新或随机。 默认不更新、非必传、False
            # | -------------------------------------------------------------------
            # | 例1: 所有媒体设备参数重新随机
            # |
            # |  "rand": True
            # |
            # | 例2: 指定媒体设备的 所有 设备参数重新随机（未指定媒体设备的设备参数不会更改）
            # |
            # |  "rand": {
            # |      "videoInputs": True
            # |  }
            # |
            # | 例3: 指定媒体设备的 指定 设备重新随机（未指定的设备参数不会更改）
            # |
            # |  "rand": {
            # |      "audioInputs": {
            # |          "device2": True
            # |      }
            # |  }
            # |
            # | 例4: 指定媒体设备的 指定 设备重新编辑（未指定的设备参数不会更改）
            # |
            # |  "rand": {
            # |      "audioOutputs": {
            # |          "device4": {
            # |              "label": "label value",
            # |              "deviceId": "deviceId value",
            # |              "groupId": "groupId value"
            # |          }
            # |      }
            # |  }
            # |
            # */
            "rand": {
                "videoInputs": True,
                "audioInputs": {  # 媒体设备的数量和设备编号必须在逻辑上合理，才能成功更新或随机。 例如： audioInputs = 2, 那么 device3 & device4 无法更新，编辑亦同
                    "device1": {  # √
                        "label": "label value",
                        "deviceId": "deviceId value",
                        "groupId": "groupId value"
                    },
                    "device2": True,  # √
                    "device3": True,  # x
                    "device4": True  # x
                },
                "audioOutputs": {
                    "device1": True,
                    "device3": True,
                    "device4": {
                        "label": "label value",
                        "deviceId": "deviceId value",
                        "groupId": "groupId value"
                    }
                }
            }
        },
        "startUrl": "",  # 其他 -> 默认首页
        "kernelVer": "96",  # 其他 -> 内核版本
        "browserSettings": {
            "pepperFlash": True,  # 其他配置 -> 启用Pepper Flash插件
            "mediaStream": True,  # 其他配置 -> 启用媒体（WebRTC音频/视频）流
            "webkitSpeech": True,  # 其他配置 -> 启用语音输入（x-webkit-speech）
            "fakeUiForMedia": True,  # 其他配置 -> 通过选择媒体流的默认设备绕过媒体流信息栏
            "gpuAndPepper3D": True,  # 其他配置 -> 启用GPU插件和Pepper 3D渲染
            "ignoreCertErrors": True,  # 其他配置 -> 忽略网站证书错误
            "audioMute": True,  # 其他配置 -> 音频静音
            "disableWebSecurity": True,  # 其他配置 -> 不强制执行同一源策略
            "disablePdf": True,  # 其他配置 -> 禁用PDF扩展
            "touchEvents": True,  # 其他配置 -> 启用对触摸事件功能检测的支持
            "hyperlinkAuditing": True  # 其他配置 -> 链接审计（hyperlink auditing）可用于追踪网站链接的点击次数
        },
        "localCache": {
            "deleteCache": True,  # 其他配置 -> 本地缓存 -> 启动浏览器前删除缓存文件
            "deleteCookie": True,  # 其他配置 -> 本地缓存 -> 启动浏览器前删除Cookie
            "clearCache": True,  # 其他配置 -> 本地缓存 -> 浏览器关闭时清理文件缓存
            "clearHistory": True  # 其他配置 -> 本地缓存 -> 浏览器关闭时删除历史记录
        },
        "synSettings": {
            "synCookie": True,  # 其他配置 -> 同步设置 -> 同步保存Cookie
            "synBookmark": True,  # 其他配置 -> 同步设置 -> 同步保存书签
            "synHistory": True,  # 其他配置 -> 同步设置 -> 同步历史记录
            "synExtension": True,  # 其他配置 -> 同步设置 -> 同步扩展插件
            "synKeepKey": True,  # 其他配置 -> 同步设置 -> 同步保存密码
            "synLastTag": True  # 其他配置 -> 同步设置 -> 同步近期标签页
        },
        "leakProof": {
            "computerName": "",  # 其他配置 -> 防泄露设置 -> 电脑名称
            "macAddress": "",  # 其他配置 -> 防泄露设置 -> Mac 地址
            "rand": [
                "computerName",  # 其他配置 -> 防泄露设置 -> 随机（需要随机的键名）
                "macAddress"
            ]
        },
        "browserParams": "",  # 其他配置 -> 自定义 -> 自定义启动浏览器参数
        "customDns": "",  # 其他配置 -> 自定义 -> 自定义DNS
        "remoteDebug": {
            "bindAllDebug": False,  # 其他配置 -> 远程调试功能 -> 端口绑定0.0.0.0
            "debuggingPort": "",  # 其他配置 -> 远程调试功能 -> 远程调试端口
            "logLevels": 99  # 其他配置 -> 远程调试功能 -> 调试日志级别：0：DEFAULT 1: VERBOSE 99: DISABLE
        },
        "pluginFingerprint": {  # 浏览插件指纹 -> 插件列表
            "pluginEnable": True,  # 浏览插件指纹 -> 启用自定义插件信息
            "list": {  # 浏览插件指纹 -> 插件列表（selected 选中的）
                # 插件名称
                "name": [
                    "Chrome PDF Plugin",
                    "Chrome PDF Viewer",
                    "Native Client",
                    "Shockwave Flash"
                ],
                # 描述
                "describe": [
                    "Portable Document Format",
                    "-",
                    "-",
                    "Shockwave Flash 32.0 r0"
                ],
                # 文件名称
                "fileName": [
                    "internal-pdf-viewer",
                    "mhjfbmdgcfjbbpaeojofohoefgiehjai",
                    "internal-nacl-plugin",
                    "pepflashplayer.dll"
                ],
                # mime type
                "mimeType": [
                    "application/x-google-chrome-pdf",
                    "application/pdf",
                    "application/x-nacl|application/x-pnacl",
                    "application/x-shockwave-flash|application/futuresplash"
                ],
                # mime 描述
                "mimeDescription": [
                    "Portable Document Format",
                    "-",
                    "Native Client Executable|-Portable Native Client Executable",
                    "Shockwave Flash|Shockwave Flash"
                ],
                # mime 扩展名
                "mimeExtension": [
                    "pdf",
                    "pdf",
                    "|",
                    "swf|spl"
                ]
            }
        },
        "unPluginFingerprint": {  # 浏览插件指纹 -> 插件列表
            "list": {  # 浏览插件指纹 -> 插件列表（未选中的）
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
        "browserApi": {  # 浏览器API 浏览器API指纹设置
            "setBatteryStatus": False,  # 设置 Battery Status API
            "isCharging": True,  # 是否正在充电
            "chargingTime": "0",  # 完成充电需要时间 "0"、 "Infinity"
            "drainsTime": "Infinity",  # 电量可以使用时间 "Infinity"、 "3600"、 "18000"、 "10800"、 "12600"
            "batteryPercentage": "1",  # 电池电量的百分比 0.01 ~ 1
            "autoGeoIp": False,  # Geolocation -> 基于IP地址填充地理位置
            "setLatitude": False,  # Geolocation -> 纬度
            "setLongitude": False,  # Geolocation -> 经度
            "setAccuracy": False,  # Geolocation -> 精度
            "latitude": "51.482594",  # Geolocation -> 纬度值
            "longitude": "-0.007661",  # Geolocation -> 经度值
            "accuracy": "1803.34",  # Geolocation -> 精度（米）
            "setWebBluetooth": False,  # 设置Web Bluetooth API
            "setBluetoothAdapter": False,  # Bluetooth Adapter
            "speechSynthesis": False,  # 设置SpeechSynthesis API
            "speechVoicesList": {  # Speech Voices 列表（selected 启用的）
                "voiceURI": [
                    "voiceURI value 1",  # string
                    "voiceURI value 2"
                ],
                "name": [
                    "name value 1",  # string
                    "name value 2"
                ],
                "lang": [
                    "lang value 1",  # string
                    "lang value 2"
                ],
                "localService": [
                    False,  # boolean
                    True
                ],
                "default": [
                    True,  # boolean
                    False
                ]
            },
            "unSpeechVoicesList": {  # Speech Voices 列表（未启用的）
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
            "speechVoicesRestoreDefault": True  # Speech Voices 恢复默认
        },
        "sslFingerprint": {  # SSL 指纹设置
            "enableCustomSSL": True,  # 启用自定义SSL 指纹
            "versionMin": 0,  # SSL Version min  0:TLSv1    1:TLSv1.1    2:TLSv1.2    3:TLSv1.3
            "versionMax": 1,  # SSL Version max  0:TLSv1.2  1:TLSv1.3
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
        "otherProtection": {  # 其他防护
            "setPortScan": True,  # 其他防护 -> 开启端口扫描保护
            "localPortsExclude": "8000,12345,42069"  # 其他防护 -> 特定端口白名单
        },
        "header": {  # Header
            "setHeaderCustom": True,  # Header -> 开启 Header 自定义
            "list": {  # Header -> Header List
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
        "cmdcfg": {  # 辅助启动
            "openCommandLine": False,  # 辅助启动 -> 开启 浏览器启动前 执行命令行
            "commandLine": "",  # 辅助启动 -> 命令行
            "closeCommandLine": True  # 辅助启动 -> 浏览器关闭终止命令行进程
        },
        "tag": "group_name"  # 组名称
    }
    return config


if __name__ == '__main__':
    create_profile()
