# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2022/8/10 1:49
# !@Author : DongHan Yang
# !@File   : GS.py

# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2022/8/7 21:51
# !@File   : FMM.py
# 正向匹配
import re

if __name__ == '__main__':
    txt_path = 'dic/mdt.txt'
    flag = 0
    rets = []
    with open(txt_path, 'r', encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line[0] == "第" and line[2] == "出":
                flag += 1
                rets.append([])
            elif flag > 0 and line[0] != "【":  # and line[0] != "〔"
                line1 = re.split(r'[，: : 。:？]', line)
                rets[flag - 1].extend(line1)
    gs, zz = [], []
    for r in rets:
        gs.append([])
        zz.append([])
        for i in range(len(r)):
            if i % 2 == 0:
                gs[-1].append(r[i])
            else:
                zz[-1].append(r[i])
    print(rets)
    print(gs)
    print(zz)
