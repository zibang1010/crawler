# -*- coding: utf-8 -*-

# @File  : scheduler.py
# @Author: zibang
# @Time  : 2月 26,2022
# @Desc
import multiprocessing
from local_crawl import LocalCrawl
import time


class Scheduler():
    def __init__(self):
        pass

    def run_cart(self):

        while True:
            c = LocalCrawl()
            c.run()
            time.sleep(1)

    def run(self):
        cart_process1 = multiprocessing.Process(target=self.run_cart)
        cart_process1.start()
        cart_process2 = multiprocessing.Process(target=self.run_cart)
        cart_process2.start()
        cart_process3 = multiprocessing.Process(target=self.run_cart)
        cart_process3.start()
        cart_process4 = multiprocessing.Process(target=self.run_cart)
        cart_process4.start()
        cart_process1.join()
        cart_process2.join()
        cart_process3.join()
        cart_process4.join()


if __name__ == '__main__':
    s = Scheduler()
    s.run()
