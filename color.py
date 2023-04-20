# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2022/8/14 19:42
# !@Author : DongHan Yang
# !@File   : js.py
import csv
import re


def writeCsv(filename, header, datas):
    fn = f'csv/{filename}.csv'
    with open(fn, 'w', encoding='utf_8_sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(datas)


startXC = False


def getQuPaiList():
    start, isFirst = False, False
    global startXC
    index, qIndex = 0, 0  # 序号（无颜色为0）、曲牌序号（递增）
    rets = []  # 输出csv列表
    rets0 = []  # '序号','剧本','出','曲牌','是否前腔','曲牌序号'
    with open(txt_path, 'r', encoding="utf_8_sig") as f:
        fist = True
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.count("下场诗"):
                startXC = True
            if line.count("注释"):
                start = False
            s = line.split()
            if s[0].split('[')[0] != '' and s[0].split('[')[0][0] == "第" and s[0].split('[')[0][-1] == "出":
                start = True
                startXC = False
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
                            print(rets0)
                        else:
                            for ret in ret3:
                                rets.append(rets0 + ret)
                                print(rets0 + ret)
                        rets0 = [index, set_name, chu, quPai, isQQ, qIndex]
                        ret3 = []
                        if fist:
                            fist = False
                    elif len(ret1) != 0:
                        ret3.extend(ret1)
    # sorted_lst = sorted(rets, key=lambda x: (x[5], x[-1]))
    sorted_data = sorted(rets, key=lambda x: (x[5], x[-1]))
    results = []
    for d in sorted_data:
        if len(d) > 6:
            results.append(d[:-1])
        else:
            results.append(d)
    print(results)
    return results


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
    isCount = 0
    # 遍历字符串中的每个字符
    for i, color in enumerate(colors):
        pattern = re.compile(color)
        match = pattern.search(line)
        while match:
            start, end = match.span()
            # print(start, end)
            mask = ((1 << (end - start)) - 1) << start  # 构造掩码，将从 start 到 end 位置为 1
            if bin(mask & isCount).count('1'):
                isCount |= mask
                match = pattern.search(line, end)
                continue
            isCount |= mask
            start_index = max(0, start - 2)
            start_i = start
            while start_i > start_index:
                if start_i - 1 >= 0 and line[start_i - 1] in ['，', '。', '！', '？', '[', ']', '）', '　', '］', '［', '【',
                                                              '】', '﹐', '“']:
                    break
                start_i -= 1
            # result.append(line[start_i:i])
            # 查找颜色后两个汉字
            end_index = min(len(line), end + 1)
            end_i = end - 1
            while end_i < end_index:
                if end_i + 1 < len(line) and line[end_i + 1] in ['，', '。', '！', '？', '[', ']', '）', '　', '］', '［', '【',
                                                                 '】', '﹐', '“']:
                    break
                end_i += 1
            # result.append([color, line[start_i:i], line[i + 1:end_i]])
            raw_data = line[start_i:end_i + 1]
            type = brackets(line, raw_data)
            all_data = get_field_with(line, raw_data)
            if all_data is None:
                print("error")
            result.append([color, raw_data.replace(" ", ""), all_data.replace(" ", ""), type, start])
            match = pattern.search(line, end)
    return result


def brackets(line, data):
    if startXC:
        return '下场诗'
    if is_in_brackets(line, data, ['【', '】']) or is_in_brackets(line, data, ['［', '］']):
        return '曲牌'
    if is_in_brackets(line, data, ['（', '）']):
        return '括号'
    return '正文'


def is_in_brackets(line, data, flags):
    """
    判断字符 data 是否在括号内。
    """
    stack = []
    begin = flags[0]
    end = flags[1]
    for i, ch in enumerate(line):
        if ch == begin:
            stack.append(i)
        elif ch == end:
            if stack:
                left_bracket_index = stack.pop()
                if line[left_bracket_index + 1:i].find(data) != -1:
                    return True
    return False


pattern = r'[，“。！？\[\]）］［【】﹐]'


def get_field_with(text, a):
    fields = re.split(pattern, text)
    for field in fields:
        if a in field:
            return field.strip()
    return None


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


# 牡丹亭、紫钗记、南柯记、邯郸记
set_name = "邯郸记"
filename = "./dic/color.txt"
if __name__ == '__main__':
    txt_path = f'dic/汤显祖{set_name}.txt'
    rets = getQuPaiList()
    # '出', '曲牌', '是否前腔', '顺序', '句式'
    writeCsv(f'{set_name}色彩', ['序号', '剧本', '出', '曲牌', '是否前腔', '曲牌序号', '色彩', '色彩全字', '色彩全句', '色彩类型'], rets)
