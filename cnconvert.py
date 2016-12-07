#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
cnconvert: Convertion between Chinese number string and integer number.
author: DongChengliang hack.dcl@gmail.com
version: 2011-9-18 1.0
license: GPL v3
bugfix: 2011-11-13
for python3k: int/int produce a float
"""


def c2n(cn):
    """ c2n(Chinese number string) -> number<int>
        将“*亿**万*千*百*十*”式的中文数字字符串转换为数字。
        注意：最大的权重为亿，兆之类的更大的权重是不支持的。
    """
    num = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6,
           '七': 7, '八': 8, '九': 9}
    weight1 = {'十': 10, '百': 100, '千': 1000}
    weight2 = {'万': 10000, '亿': 100000000}  # 万and亿 need special treatment

    result = 0
    resultbeyondyi = 0  # 处理“*亿**万***”之类时需要将过亿部分单独计算
    count = []  # supporting stack, store the value need be weighted.

    for c in cn:
        if c in num:
            count.append(num[c])
        elif c in weight1:
            if c == '十' and len(count) == 0:
                count.append(1)
            try:
                result += count.pop() * weight1[c]
            except:
                raise Exception("'%s': not a valid Chinese number string." % cn)
        elif c in weight2:
            if len(count) > 0:
                result += count.pop()
            if c == '亿':
                resultbeyondyi = result * weight2[c]
                result = 0
            result *= weight2[c]
        elif c == '零' or c == '〇':
            pass
        else:
            raise Exception("'%s' in '%s': illegal character in Chinese number string." % (c, cn))
    if len(count) > 0:
        result += count.pop()

    return result + resultbeyondyi


def n2c(int_number):
    """ Convert int number to Chinese number string. i.e. 342 -> 三百四十二
    """
    try:
        int_number = int(int_number)
    except:
        print('n2c need a int parameter, however it is %s' % int_number)
        raise

    num = {0: '零', 1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '七', 8: '八', 9: '九'}
    weight = ['', '十', '百', '千']

    n = int_number  # for abbreviation
    result = ''

    if n == 0:  # [0]
        return num[n]

    if n >= 100000000:  # [100000000, )
        result += n2c(n / 100000000) + '亿'
        if n % 100000000 != 0:
            if n % 100000000 < 10000000:
                result += num[0]
            result += n2c(n % 100000000)
    elif n >= 10000:  # [10000,99999999]
        result += n2c(n / 10000) + '万'
        if n % 10000 != 0:
            if n % 10000 < 1000:
                result += num[0]
            result += n2c(n % 10000)
    else:  # [1,9999]
        for c in weight:
            if n % 10 == 0:  # special treatment for number 0
                # if result still empty(i.e. 9000) or already has a 0(i.e. 9003), skip this 0
                if not result or result[0] == num[0]:
                    pass
                # else put a '零'
                else:
                    result = num[0] + result
            else:
                # normal situation: put this number in Chinese and its weight
                result = num[n % 10] + c + result
            if n / 10 < 1:
                break
            else:
                n = int(n / 10)  # cautions! python 3k: int/int produce a float!
        if int_number >= 10 and int_number <= 19:  # special treatment: 一十三 -> 十三
            result = result[1:]

    return result
