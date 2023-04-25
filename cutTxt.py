# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2022/8/14 19:42
# !@Author : DongHan Yang
# !@File   : js.py
import csv
import ebooklib
from ebooklib import epub
from lxml import html
import re


def write_txt(set_name):
    txt_path = f'dic/汤显祖戏曲全集{set_name}.epub'
    book = epub.read_epub(txt_path)
    # 遍历所有章节
    all_text = ""
    for item in book.get_items():
        # 只处理HTML页面
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            chapter_content = item.get_content()
            root = html.fromstring(chapter_content)
            # for a in root.xpath("//a"):
            #     a.text = None
            for element in root.xpath('//span[contains(@class, "font2")]'):
                if element.text is not None:
                    remove_newlines(element)
                    element.text = '{' + element.text + '}'
                    element.attrib.pop('class', None)
                    element.set('style', 'font-weight: bold;')
            for element in root.xpath('//span[@class="kindle-cn-bold"]'):
                remove_newlines(element)
            for element in root.xpath('//p[contains(@class, "kindle-cn-kai")]'):
                txt = element.xpath('.//text()')
                contains = any([s in ''.join(txt) for s in ["［", "【"]])
                if contains:
                    element.text = 'B' + element.text  # 宾白
                else:
                    element.text = 'G' + element.text  # 段落
                element.tail = '*' + element.tail
            for element in root.xpath('//span[@class="kindle-cn-kai"]'):
                if element.text is not None:
                    remove_newlines(element)
                    element.text = '#' + element.text + '*'
                    # print(element.text)
            for child in root.xpath('//a'):
                remove_newlines(child)
            for child in root.xpath('//img'):
                child.text = 'P'
                remove_newlines(child)
            for child in root.xpath('//sup'):
                remove_newlines(child)
            paragraph_text = html.tostring(root, encoding='unicode', method='text')
            # paragraph_text = re.sub(r'\r\n', '', paragraph_text)
            all_text += paragraph_text
    # 保存文本到文件
    with open(f'./dic/{set_name}.txt', 'w', encoding='utf-8') as f:
        f.write(all_text)


def remove_newlines(child):
    if child.head is not None:
        child.head.tail = child.head.tail.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')
    if child.text is not None:
        child.text = child.text.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')
    if child.tail is not None:
        child.tail = child.tail.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')


# 牡丹亭、紫钗记、南柯记、邯郸记
if __name__ == '__main__':
    for i in ['南柯记', '牡丹亭', '邯郸记', '紫钗记', ]:  # '南柯记', '牡丹亭',
        write_txt(i)
