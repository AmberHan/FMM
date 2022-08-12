# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2022/8/7 21:51
# !@File   : FMM.py
# 正向匹配
import re
import csv


class leftMax(object):
    def __init__(self, dict_path):
        self.dictionary = set()  # 定义字典
        self.maximum = 5  # 最大匹配长度
        self.pre = None  # 记录上一次【】词牌
        with open(dict_path, 'r', encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                self.dictionary |= set(line.split('\t'))
                # self.dictionary.add(line.split('\t')[1])
                # if len(line) > self.maximum:
                #     self.maximum = len(line)

    def cut(self, text):
        # result = []
        results = []
        length = len(text)
        index = 0
        while length > 0:
            word = None
            for size in range(self.maximum, 0, -1):
                if length - size < 0:
                    continue
                piece = text[index:index + size]
                if piece in self.dictionary:  # or list(piece) == "前腔"
                    if piece == "前腔":
                        piece = self.pre
                    if text[index + size] == "】":
                        word = piece
                        self.pre = word
                        results.append(word)
                    elif text[index + size] == "〕":
                        word = piece
                        results.append(word)
                    length -= size
                    index += size
                    break
            if word is None:
                length -= 1
                index += 1
        return results


# 逆向匹配
class rightMax(object):
    def __init__(self, dict_path):
        self.dictionary = set()  # 定义字典
        self.maximum = 3  # 最大匹配长度

        with open(dict_path, 'r', encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # self.dictionary.add(line.split('\t')[1])
                self.dictionary |= set(line.split('\t'))
                # if len(line) > self.maximum:
                #     self.maximum = len(line)

    def cut(self, text):
        result = []
        results = []
        index = len(text)
        while index > 0:
            word = None
            for size in range(self.maximum, 0, -1):
                if index - size < 0:
                    continue
                piece = text[(index - size):index]
                if piece in self.dictionary:  # or list(piece) == "前腔"
                    # if piece == "前腔":
                    #     piece = results[-1]
                    word = piece
                    results.append(word)
                    index -= size
                    break
            if word is None:
                result.append(text[(index - 1):index])
                index -= 1
        return results[::-1]  # 由于append为添加至末尾，故需反向打印


# 双向匹配
def doubleMax(text, path):
    left = leftMax(path)
    right = rightMax(path)

    leftMatch = left.cut(text)
    rightMatch = right.cut(text)

    # 返回分词数较少者
    if (len(leftMatch) != len(rightMatch)):
        if (len(leftMatch) < len(rightMatch)):
            return leftMatch
        else:
            return rightMatch
    else:  # 若分词数量相同，进一步判断
        leftsingle = 0
        rightsingle = 0
        isEqual = True  # 用以标志结果是否相同
        for i in range(len(leftMatch)):
            if (leftMatch[i] != rightMatch[i]):
                isEqual = False
            # 统计单字数
            if (len(leftMatch[i]) == 1):
                leftsingle += 1
            if (len(rightMatch[i]) == 1):
                rightsingle += 1
        if (isEqual):
            return leftMatch
        if (leftsingle < rightsingle):
            return leftMatch
        else:
            return rightMatch


# 获取字典
def get_txt(words):
    with open(words, 'r', encoding='gbk', ) as f:
        try:
            file_content = f.read().split()
        finally:
            f.close()
    chars = list(set(file_content))
    return chars


# def changeData(lst):
#     for l in lst:
#         for index in range(len(l)):
#             s = l[index]
#             if s == "前腔":
#                 l[index] = l[index - 1]
#     return lst

def write_csv(filename, header, datas):
    fn = f'csv/{filename}.csv'
    with open(fn, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(datas)


if __name__ == '__main__':
    tokenizer = leftMax('dic/cpm.txt')
    # tokenizer = rightMax('dic/cpm.txt')
    txt_path = 'dic/mdt.txt'
    flag = 0
    rets = []  # 关系
    rets0 = []  # 戏曲名牡丹亭
    rets1 = set()  # 词牌名
    with open(txt_path, 'r', encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.split()[0][0] == "第" and line.split()[0][-1] == "出":
                flag += 1
                rets0.append(line.split())
                rets0[-1].append('牡丹亭')
                rets.append([])
            if flag > 0:
                # line = re.split(r'[，:。]', line)
                la = tokenizer.cut(line)
                if la is not None:
                    rets[- 1].extend(la)
                    rets1 |= set(la)
    # 戏曲名
    print("戏曲名：", rets0)
    write_csv('牡丹亭', ['章节', '标题', '戏曲名'], rets0)
    # 词牌名
    rets3 = []
    print("所有词牌名", rets1)
    for r in rets1:
        rets3.append([r])
    print("每一出词牌名", rets3)
    write_csv('词牌名', ['词牌名'], rets3)
    # 戏曲和词牌名关系
    print("关系列表：", rets)
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
    write_csv('牡丹亭_词牌名', ['章节', '次数', '词牌名'], rets4)
    # write_csv()
    # print(changeData(rets))
    # print(doubleMax(text, 'dic/cpm.txt'))
