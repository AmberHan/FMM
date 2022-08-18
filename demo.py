# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2022/8/13 20:27
# !@Author : DongHan Yang
# !@File   : demo.py
import re

line = "第一出[1] 你好[2]"
print(line)
s = line.split()
if s[0].split('[')[0][0] == "第" and s[0].split('[')[0][-1] == "出":
    print([s[0].split('[')[0], s[1].split('[')[0]])
# ret = re.split(r"[\w]", line)
# print(ret)
