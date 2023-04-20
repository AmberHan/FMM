# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2022/8/14 19:42
# !@Author : DongHan Yang
# !@File   : js.py
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
                    if quPai != "":
                        isHan = False  # 判断前腔中文
                        if line[nextIndex[0]] == '】':
                            isHan = True
                        quJs, quChen, quBin, quChang = getQuPaiJs(line, nextIndex)
                        isQQ = "否" if quPai != "前腔" else "是"
                        quPai = quPai if quPai != "前腔" else pre
                        seq += 1
                        quJs = [0] if quJs == [] else quJs
                        quChen = [0] if quChen == [] else quChen
                        quBin = [0] if quBin == [] else quBin
                        quChang = [0] if quChang == [] else quChang
                        rets0 = [chu, quPai, isQQ, seq, quJs, quChen, quBin, quChang]
                        if isHan:
                            pre = quPai
                        # 如果取消分列；取消下面两行代码
                        # for ret in quJs:
                        #     rets0.append(ret)
                        rets.append(rets0)
    print("Csv:", rets)
    return rets


def isEnd(word, flag1, flag2):
    if word is "{":
        flag1 = True
    if word is "}":
        flag1 = False
    if word is "#":
        flag2 = True
    if word is "*":
        flag2 = False
    return flag1, flag2


# 输入：line：一行内容; nextIndex: 起始位;
# 输出：quPai: 曲牌字数列表
def getQuPaiJs(line, nextIndex):
    quPai = ""
    chen, bin, chang = "", "", ""
    quPaiList = []
    chenList, binList, changList = [], [], []
    totalNum = 0
    flag1, flag2 = False, False  # flag1 {承字}；flag2 #宾白*
    for index in range(nextIndex[0] + 1, len(line)):
        word = line[index]
        if word in ["{", "#", "}", "*"]:
            flag1, flag2 = isEnd(word, flag1, flag2)
            continue
        if word in ["“", "”", "《", "》", " "]:
            continue
        if word in ["【", "[", "［"] and index + 1 < len(line) and isChinese(line[index + 1]):
            nextIndex[0] = index
            return quPaiList, chenList, binList, changList
        if word in ["【", "[", "(", "（", "［"]:
            totalNum += 1
        elif word in ["]", "】", ")", "）", "］"]:
            totalNum -= 1
        elif totalNum == 0 and not isChinese(word):
            quPaiList.append(len(quPai))
            chenList.append(len(chen))
            binList.append(len(bin))
            changList.append(len(chang))
            quPai = ""
            chen, bin, chang = "", "", ""
            if len(quPai) != len(chen) + len(bin) + len(chang):
                print('err')
        elif totalNum == 0 and isChinese(word):
            quPai += word
            if flag1:
                chen += word
            elif flag2:
                bin += word
            else:
                chang += word
    nextIndex[0] = -1
    return quPaiList, chenList, binList, changList


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
    elif (uchar >= u'\u0020' and uchar <= u'\u007f') or (u'\u2000' and uchar <= u'\u206f') \
            or (uchar >= u'\u3000' and uchar <= u'\u303f') or (u'\uff00' and uchar <= u'\uffef'):
        return False
    else:
        return True


if __name__ == '__main__':
    for i in ['南柯记', '牡丹亭', ]:  # '紫钗记', '邯郸记'
        set_name = i
        # set_name = '牡丹亭'
        txt_path = f'dic/{set_name}.txt'
        rets = getQuPaiList()
        writeCsv(f'{set_name}句式', ['出', '曲牌', '是否前腔', '顺序', '全部句式', '承词', '宾白', '唱词'], rets)
