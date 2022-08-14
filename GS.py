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
import csv


def write_csv(filename, header, datas):
    fn = f'csv/{filename}.csv'
    with open(fn, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(datas)


if __name__ == '__main__':
    txt_path = 'dic/mdt.txt'
    flag = 0
    rets0 = []
    rets = []
    with open(txt_path, 'r', encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.split()[0][0] == "第" and line.split()[0][-1] == "出":
                rets.append([])
                rets0.append(line.split()[0])
            elif line[0] != "【":  # and line[0] != "〔"
                line1 = re.split(r'[，: : 。:？]', line)
                if len(line1) == 4:
                    rets[- 1].extend(line1)
        rets[0][1] = rets[0][3] = rets[0][5] = rets[0][7] = "王实辅"
    gs, zz = [], []
    for r in rets:
        gs.append([])
        zz.append([])
        for i in range(len(r)):
            if i % 2 == 0:
                gs[-1].append(r[i])
            else:
                zz[-1].append(r[i])
    # print(rets)
    print(gs)
    print(zz)
    # 创建作者实体
    zset = set()
    for z in zz:
        zset |= set(z)
    # print(zset)
    rets3 = []
    for r in zset:
        rets3.append([r])
    write_csv('诗人', ['诗人'], rets3)
    # 牡丹亭_作者
    rets4 = []
    i = 0
    for z in zz:
        z_set = set(z)
        for cp in z_set:
            pro_num = z.count(cp)
            rets4.append([rets0[i], pro_num, cp])
        i += 1
    write_csv('牡丹亭_诗人', ['章节', '出现次数', '诗人'], rets4)
