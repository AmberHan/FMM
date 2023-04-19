# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2022/8/14 19:42
# !@Author : DongHan Yang
# !@File   : js.py
import csv
import ebooklib
from ebooklib import epub
from lxml import html

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
                        quJs = getQuPaiJs(line, nextIndex)
                        isQQ = "否" if quPai != "前腔" else "是"
                        quPai = quPai if quPai != "前腔" else pre
                        seq += 1
                        quJs = [0] if quJs == [] else quJs
                        rets0 = [chu, quPai, isQQ, seq, quJs]
                        if isHan:
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
        if word in ["“", "”", "《", "》", " "]:
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
    elif (uchar >= u'\u0020' and uchar <= u'\u007f') or (u'\u2000' and uchar <= u'\u206f') \
            or (uchar >= u'\u3000' and uchar <= u'\u303f') or (u'\uff00' and uchar <= u'\uffef'):
        return False
    else:
        return True


if __name__ == '__main__':
    set_name = "牡丹亭"
    txt_path = f'dic/汤显祖戏曲全集{set_name}.epub'
    book = epub.read_epub(txt_path)

    # 遍历所有章节
    all_text = ""
    for item in book.get_items():
        # 只处理HTML页面
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            # 获取页面的内容
            chapter_content = item.get_content()
            # 将XHTML文本转换为HTML元素
            root = html.fromstring(chapter_content)
            # 遍历HTML元素中的所有<span>元素
            for element in root.xpath('//span[@class="font2"]'):
                # 替换文本中的<span>元素，加上感叹号
                if element.text is not None:
                    element.text = '@' + element.text + '@'
                    # 将<span>元素的class属性移除，加上style属性
                    element.attrib.pop('class', None)
                    element.set('style', 'font-weight: bold;')
            for element in root.xpath('//span[@class="kindle-cn-kai"]'):
                # 替换文本中的<span>元素，加上感叹号
                if element.text is not None:
                    element.text = '%' + element.text + '%'
                    # 将<span>元素的class属性移除，加上style属性
                    element.attrib.pop('class', None)
                    element.set('style', 'font-weight: bold;')
            # 遍历HTML元素中的所有<p>元素
            paragraph_text = html.tostring(root, encoding='unicode', method='text')
            all_text += paragraph_text

    # 保存文本到文件
    with open('output.txt', 'w', encoding='utf-8') as f:
        f.write(all_text)

    # rets = getQuPaiList()
    # writeCsv(f'{set_name}句式', ['出', '曲牌', '是否前腔', '顺序', '句式'], rets)
