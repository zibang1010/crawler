# -*- coding: utf-8 -*-

# @File  : test_demo.py
# @Author: zibang
# @Time  : 2月 26,2022
# @Desc
from playwright.sync_api import sync_playwright


def run():
    with sync_playwright() as p:
        browsers = p.chromium.launch_persistent_context(
            user_data_dir='D:/zibang/projects/crawler/spiders/chromeProfile',
            headless=False,
            executable_path='D:/app/VMLogin/chrome/96.0.4664.45/chrome.exe'
        )
        page = browsers.new_page()
        page.add_init_script(path='./script/demo.js')
        page.goto('https://www.ip138.com/')
        page.wait_for_timeout(600 * 1000)


if __name__ == '__main__':
    run()
