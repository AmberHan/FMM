# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2022/8/9 1:42
# !@Author : DongHan Yang
# !@File   : 1.py

txt_path = 'dic/mdt.txt'


def pp(a, b):
    rets = []
    with open(txt_path, 'r', encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            pos = line.find(a)
            while pos != -1:
                # if pos != -1:
                f = pos
                pos = line.find(b, pos + 1)
                if line[f + 1: pos] not in rets:
                    rets.append(line[f + 1: pos])
                pos = line.find(a, pos + 1)
    print(rets)


def ff(s, p):
    p1 = s.find("【", p)
    p2 = s.find("〔", p)
    if p1 == -1:
        return p2
    if p2 == -1:
        return p1
    return p1 if p1 < p2 else p2


def ll(s, p):
    p1 = s.find("】", p)
    p2 = s.find("〕", p)
    if p1 == -1:
        return p2
    if p2 == -1:
        return p1
    return p1 if p1 < p2 else p2


def pp1():
    rets = []
    with open(txt_path, 'r', encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            pos = ff(line, 0)
            while pos != -1:
                f = pos
                pos = ll(line, pos + 1)
                if line[f + 1: pos] not in rets:
                    rets.append(line[f + 1: pos])
                pos = ff(line, pos + 1)
    print(rets)


# pp("【", "】")
# pp("〔", "〕")
pp1()
