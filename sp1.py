# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2022/8/9 1:42
# !@Author : DongHan Yang
# !@File   : sp.py
import re
import csv


def write_csv(filename, header, datas):
    fn = f'csv/{filename}.csv'
    with open(fn, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(datas)


def pp(chooseList):
    start = False
    rets = []  # 关系
    rets0 = []  # 戏曲名牡丹亭
    rets1 = set()  # 词牌名
    with open(txt_path, 'r', encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.count("注释"):
                start = False
            if line.split()[0][0] == "第" and line.split()[0][-1] == "出":
                start = True
                rets0.append(line.split())
                rets0[-1].append('牡丹亭')
                rets.append([])
            if start:
                line1 = re.findall(r"[［|【]+(\w+)+[］|】]", line)
                rets[- 1].extend(line1)
                rets1 |= set(line1)
    print("牡丹亭章节：", rets0)
    print("词牌名：", rets1)
    print("关系：", rets)
    return rets0, rets1, rets


if __name__ == '__main__':
    txt_path = 'dic/汤显祖牡丹亭.txt'
    rets0, rets1, rets = pp(["【", "】", "[", "]"])
    # 牡丹亭
    write_csv('牡丹亭', ['章节', '标题', '戏曲名'], rets0)
    # 词牌名
    rets3 = []
    for r in rets1:
        rets3.append([r])
    write_csv('词牌名', ['词牌名'], rets3)
    # 关系
    rets4 = []
    i = 0
    for cps in rets:
        zj = rets0[i][0]
        i += 1
        cps_set = set(cps)
        for cp in cps_set:
            pro_num = cps.count(cp)
            rets4.append([zj, pro_num, cp])
    write_csv('牡丹亭_词牌名', ['章节', '次数', '词牌名'], rets4)
