#coding=utf-8
def suffix(start, end):
    """
    start(int) end(int) 构造待发送的文件名后缀：230-235 表示从230章到235章
    """
    suf = ""
    if start == end:
        suf = str(start)
    else:
        suf = str(start) + "-" + str(end)
    return suf


def is_chi(self, text):
    """判断是否为中文"""
    return all('\u4e00' <= char <= '\u9fff' for char in text)