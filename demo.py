# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2022/8/13 20:27
# !@Author : DongHan Yang
# !@File   : demo.py
import re
line = "［汉宫春］杜宝黄［w］堂[W]，生【丽娘】小姐，爱踏春阳。感梦书生折柳，竟为情伤。写真留记[13]，葬梅花道院凄凉。三年上，有梦梅柳子，于此赴高唐[14]。果尔回生定配，赴临安取试，寇起淮扬。正把杜公围困，小姐惊惶。教柳郎行探，反遭疑激恼平章[15]。风流况[16]，施行正苦[17]，报中状元郎。"
print(line)
ret = re.findall(r"[【]+(\w+)+[】]", line)
print(ret)