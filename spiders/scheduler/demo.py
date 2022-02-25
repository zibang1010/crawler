# -*- coding: utf-8 -*-

# @File  : demo.py
# @Author: zibang
# @Time  : 2月 25,2022
# @Desc  :
list1 = ["one", "two", "three", "four", "five"]

list2 = ["one", "three", "two", "four"]

print(set(list1).difference(set(list2)))

# set(list2).difference(set(list1))
