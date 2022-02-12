# -*- coding: utf-8 -*-

# @File  : demo.py
# @Author: zibang
# @Time  : 2月 06,2022
# @Desc
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir='D:/zibang/projects/crawler/TI/profile',
        channel='chrome',
        executable_path='D:/app/VMLogin/chrome/96.0.4664.45/chrome.exe',
        headless=False,
        args=[
            '--disable-blink-features=AutomationControlled',
            '--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0"',
            '--no-first-run',
            '--lang=zh-TW',
            '--vmlogin-name=RGVtbw==',
            '--webgldata',
            '--canvas-fp=2',
            '--clientrects-fp',
            '--vmfont-fp',
            '--dynamic-font',
            '--lan-ip=192.168.51.77',
            '--audio-fp',
            '--swidth=1280',
            '--sheight=720',
            '--window-size=1280,680',
            '--pixelratio=1.0',
            '--n-platform=Win64',
            '--n-product=Gecko',
            '--n-appname=Netscape',
            '--n-accetplang=zh-TW,zh;q=0.9',
            '--n-concurrent=4',
            '--taskbar_height=40',
            '--n-vendor',
            '--n-productsub=20100101',
            '--n-appver="5.0',
            '--n-memory=8',
            '--timezoneid=Asia/Shanghai',
            '--n-wssscan',
            '--audio-input-num=2',
            '--audio-output-num=2',
            '--video-intput-num=1',
            '--enable-media-stream=1',
            '--enable-speech-input=1',
            '--disable-gpu',
            '--disable-gpu-compositing',
            '--touch-events=disabled',
            '--remote-debugging-port=16823',
            '--no-sandbox',
            '--disable-features=ExtensionsToolbarMenu,FlashDeprecationWarning',
            '--l-port=5309',
            '--metrics-recording-only',
            '--force-color-profile=srgb',
            '--disable-domain-reliability',
            '--password-store=basic',
            '--computer-name=QkkxREpXVFJMS1c0',
            '--mac-address=59-1D-93-01-00-04',
            '--wan-ip=8.210.102.250',
            '--g-latitude=22.2908',
            '--g-longitude=114.1501',
            '--flag-switches-begin',
            '--flag-switches-end',
        ],
        ignore_default_args=['--enable-automation'],

    )
    page = browser.new_page()
    page.goto(
        'https://fingerprintjs.github.io/fingerprintjs/'
        # 'chrome://version'
    )
    page.wait_for_timeout(60 * 1000)
    browser.close()
