# -*- coding: utf-8 -*-

# @File  : test_demo1.py
# @Author: zibang
# @Time  : 2月 13,2022
# @Desc
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir='D:/zibang/projects/crawler/TI/fingerprint/profile',
        headless=False,
        executable_path='D:/app/VMLogin/chrome/92.0.4515.131/chrome.exe'
    )
    browser.add_init_script(path='demo.js')
    page = browser.new_page()
    page.goto('https://www.baidu.com')

