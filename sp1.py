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


def pp(chooseList,set_name):
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
            # print(line)
            # if line.split()[0][0] == "第" and line.split()[0][-1] == "出":
            s = line.split()
            if s[0].split('[')[0] != '' and s[0].split('[')[0][0] == "第" and s[0].split('[')[0][-1] == "出":
                start = True
                rets0.append([s[0].split('[')[0], s[1].split('[')[0]])
                rets0[-1].append(set_name)
                rets.append([])
            if start:
                # 如果不是前腔，更新
                line2 = re.findall(r"[【]+(\w+)+[】]", line)
                if line2 and line2[0] != "前腔":
                    pre = line2[0]
                line1 = re.findall(r"[［|【]+(\w+)+[］|】]", line)
                if line1 and line1[0] == "前腔":
                    line1[0] = pre
                rets[- 1].extend(line1)
                rets1 |= set(line1)
    print(f"{set_name}章节：", rets0)
    print("曲牌名：", rets1)
    return rets0, rets1, rets


if __name__ == '__main__':
    set_name = "牡丹亭"
    txt_path = f'dic/汤显祖{set_name}.txt'
    rets0, rets1, rets = pp(["【", "】", "[", "]"], set_name)
    # 牡丹亭
    node1_name = f'{set_name}出'
    write_csv(node1_name, ['章节', '标题', '戏曲名'], rets0)
    # 词牌名
    rets3 = []
    for r in rets1:
        rets3.append([r])
    node2_name = f'{set_name}曲牌名'
    write_csv(node2_name, ['曲牌名'], rets3)
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
    print("关系：", rets4)
    write_csv(f'{node1_name}_{node2_name}', ['章节', '次数', '词牌名'], rets4)
