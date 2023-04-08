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
    start, isFirst = False, False
    index, qIndex = 0, 0  # 序号（无颜色为0）、曲牌序号（递增）
    rets = []  # 输出csv列表
    rets0 = []  # '序号','剧本','出','曲牌','是否前腔','曲牌序号'
    with open(txt_path, 'r', encoding="utf_8_sig") as f:
        fist = True
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
            elif start:
                nextIndexRec = [0]
                while (nextIndexRec[0] != -1):
                    preIndx = nextIndexRec[0]
                    quPai = getQupai(line, nextIndexRec, ["［", "[", "【"], ["］", "]", "】"])
                    ret1 = getLineColors(line, preIndx, nextIndexRec[0] + 1)
                    if quPai != "":
                        if fist:
                            ret3 = []
                        isHan = False  # 判断前腔中文
                        if line[nextIndexRec[0]] == '】':
                            isHan = True
                        isQQ = "否" if quPai != "前腔" else "是"
                        quPai = quPai if quPai != "前腔" else pre
                        if isHan:
                            pre = quPai
                        # 处理两个序号
                        qIndex += 1
                        index += 1
                        if len(ret3) == 0 and not fist:
                            index -= 1
                            rets0[0] = 0
                            rets.append(rets0)
                            print([rets0])
                        else:
                            for ret in ret3:
                                rets.append([rets0 + ret])
                                print([rets0 + ret])
                        rets0 = [index, set_name, chu, quPai, isQQ, qIndex]
                        ret3 = []
                        if fist:
                            fist = False
                    elif len(ret1) != 0:
                        ret3.extend(ret1)
    print("Csv:", rets)
    return rets


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


# 输入：line：一行内容; preIndx: 起始位; nextIndex: 中止标志
# 输出：'色彩','色彩前两字','色彩后两字','色彩类型'
def getLineColors(line, preIndx, nextIndex):
    # 全部的一行
    if nextIndex == 0:
        return getLineColor(line)
    else:
        return getLineColor(line[preIndx:nextIndex])


def getLineColor(line):
    # 定义颜色列表和结果列表
    colors = readColor()
    result = []
    # 遍历字符串中的每个字符
    i = 0
    while i < len(line):
        # 检查当前字符是否是颜色列表中的一个颜色的第一个字符
        if line[i] in colors:
            # 遍历颜色列表，检查当前字符是否是某个颜色的第一个字符
            for j in range(len(colors)):
                if line[i] == colors[j]:
                    # 如果是，将颜色添加到结果列表中
                    color = colors[j]
                    # 查找颜色前两个汉字
                    start_index = max(0, i - 2)
                    start_i = i
                    while start_i > start_index:
                        if start_i - 1 > 0 and line[start_i - 1] in ['，', '。', '！', '？', '[', ']', '）', '　']:
                            break
                        start_i -= 1
                    # result.append(line[start_i:i])
                    # 查找颜色后两个汉字
                    end_index = min(len(line), i + 3)
                    end_i = i
                    while end_i < end_index:
                        if end_i + 1 < len(line) and line[end_i + 1] in ['，', '。', '！', '？', '[', ']', '）', '　']:
                            break
                        end_i += 1
                    # result.append([color, line[start_i:i], line[i + 1:end_i]])
                    result.append([color, line[start_i:end_i]])
                    # 更新i的值，继续查找下一个字符
                    i = end_i
        # 如果当前字符不是颜色列表中的颜色，则继续查找下一个字符
        i += 1
    # 返回结果列表
    # if len(result) != 0:
    #     print(result)
    return result


# 得到颜色字典
def readColor():
    with open(filename, 'r', encoding='utf_8_sig') as f:
        content = f.read()
    word_list = [word.strip() for word in content.split()]
    return word_list


"""判断一个unicode是否是汉字"""


def isChinese(uchar):
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    elif (uchar >= u'\u0020' and uchar <= u'\u007f') or (u'\u2000' and uchar <= u'\u206f') \
            or (uchar >= u'\u3000' and uchar <= u'\u303f') or (u'\uff00' and uchar <= u'\uffef'):
        return False
    else:
        return True


set_name = "牡丹亭"
filename = "./dic/color.txt"
if __name__ == '__main__':
    txt_path = f'dic/汤显祖{set_name}.txt'
    rets = getQuPaiList()
    # '出', '曲牌', '是否前腔', '顺序', '句式'
    # writeCsv(f'{set_name}句式', ['序号','剧本','出','曲牌','是否前腔','曲牌序号','色彩','色彩前两字','色彩后两字','色彩类型'], rets)
