# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2022/8/14 19:42
# !@Author : DongHan Yang
# !@File   : js.py
import csv
import ebooklib
from ebooklib import epub
from lxml import html


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
            for element in root.xpath('//span[@class="font2"]'):
                if element.text is not None:
                    element.text = '{' + element.text + '}'
                    element.attrib.pop('class', None)
                    element.set('style', 'font-weight: bold;')
            for element in root.xpath('//span[@class="kindle-cn-kai"]'):
                if element.text is not None:
                    element.text = '#' + element.text + '*'
                    element.attrib.pop('class', None)
                    element.set('style', 'font-weight: bold;')
            paragraph_text = html.tostring(root, encoding='unicode', method='text')
            all_text += paragraph_text
    # 保存文本到文件
    with open(f'./dic/{set_name}.txt', 'w', encoding='utf-8') as f:
        f.write(all_text)


# 牡丹亭、紫钗记、南柯记、邯郸记
if __name__ == '__main__':
    for i in ['南柯记', '牡丹亭', '紫钗记', '邯郸记']:
        write_txt(i)
