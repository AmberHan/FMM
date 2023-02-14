# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2022/8/14 19:42
# !@Author : DongHan Yang
# !@File   : js.py
import re
import csv


def writeCsv(filename, header, datas):
    fn = f'csv/{filename}.csv'
    with open(fn, 'w', encoding='utf_8_sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(datas)


def getQuPaiList():
    start = False
    rets = []  # 输出csv列表
    rets0 = []  # 出-曲牌-是否前腔-字数
    with open(txt_path, 'r', encoding="utf_8_sig") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.count("注释"):
                start = False
            s = line.split()
            if s[0].split('[')[0] != '' and s[0].split('[')[0][0] == "第" and s[0].split('[')[0][-1] == "出":
                start = True
                chu = s[0].split('[')[0]  # get 出
                seq = 0  # 顺序
            elif start:
                nextIndex = [0]
                while (nextIndex[0] != -1):
                    quPai = getQupai(line, nextIndex, ["［", "[", "【"], ["］", "]", "】"])
                    quJs = getQuPaiJs(line, nextIndex)
                    if quPai != "":
                        quPai = quPai if quPai != "前腔" else pre
                        seq += 1
                        quJs = [0] if quJs==[] else quJs
                        rets0 = [chu, quPai, "否" if quPai != "前腔" else "是", seq, quJs]
                        pre = quPai
                        # 如果取消分列；取消下面三行代码
                        for ret in quJs:
                            rets0.append(ret)
                        rets.append(rets0)
    print("Csv:", rets)
    return rets


# 输入：line：一行内容; nextIndex: 起始位;
# 输出：quPai: 曲牌字数列表
def getQuPaiJs(line, nextIndex):
    quPai = ""
    quPaiList = []
    totalNum = 0
    for index in range(nextIndex[0] + 1, len(line)):
        word = line[index]
        if word in ["“", "”", "《", "》"]:
            continue
        if word in ["【", "[", "［"] and index + 1 < len(line) and isChinese(line[index + 1]):
            nextIndex[0] = index
            return quPaiList
        if word in ["【", "[", "(", "（", "［"]:
            totalNum += 1
        elif word in ["]", "】", ")", "）", "］"]:
            totalNum -= 1
        elif totalNum == 0 and not isChinese(word):
            quPaiList.append(len(quPai))
            quPai = ""
        elif totalNum == 0 and isChinese(word):
            quPai += word
    nextIndex[0] = -1
    return quPaiList


# 输入：line：一行内容; nextIndex: 起始位; sFlag: 起始标志; eFlag: 中止标志
# 输出：quPai: 曲牌
def getQupai(line, nextIndex, sFlag, eFlag):
    isStart, isEnd, quPai = False, False, ""
    for index in range(nextIndex[0], len(line)):
        word = line[index]
        if word in sFlag:
            isStart, isEnd = True, False
        elif word in eFlag:
            isStart, isEnd = False, True
            # print(quPai)
            if quPai != "" and isChinese(quPai[0]):
                nextIndex[0] = index
                return quPai
        if isStart and isChinese(word):
            quPai += word
    nextIndex[0] = -1
    return quPai


"""判断一个unicode是否是汉字"""


def isChinese(uchar):
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False


if __name__ == '__main__':
    set_name = "牡丹亭"
    txt_path = f'dic/汤显祖{set_name}.txt'
    rets = getQuPaiList()
    writeCsv(f'句式', ['出', '曲牌', '是否前腔', '顺序', '句式'], rets)
