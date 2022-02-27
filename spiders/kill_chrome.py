# -*- coding: utf-8 -*-

# @File  : kill_chrome.py
# @Author: zibang
# @Time  : 2月 26,2022
# @Desc
import os
import datetime
import time

if __name__ == '__main__':
    while True:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        os.system('taskkill /f /t /im chrome.exe')
        time.sleep(60 * 60 * 1)
