# -*- coding: UTF-8 -*-
# lvjiyong on 2015/4/20.
import re


def search(pattern, txt):
    """txt中搜索pattern"""

    _pattern = re.compile(pattern, re.IGNORECASE | re.MULTILINE)
    _match = re.search(_pattern, txt)
    if _match:
        return _match.group(1)


def replace(pattern, repl, txt):
    _pattern = re.compile(pattern, re.IGNORECASE | re.MULTILINE)
    return re.sub(_pattern, repl, txt)


def match_encoding(html):
    """从文本中获取charset编码"""
    pattern_str = "text/html;\s*charset=([a-z\d-]{2,10})"
    group = search(pattern_str, html)
    if group is None:
        pattern_str = 'charset="([a-z\d-]{2,10})"'
        group = search(pattern_str, html)
    return group


def find_all(pattern, source):
    """正则查找匹配组集合"""
    p = re.compile(pattern, re.M | re.I)
    m = re.findall(p, source)
    return m


def match(pattern, source, index):
    """查找匹配字符串返回group(1)值"""
    p = re.compile(pattern, re.M)
    _match = p.search(source)
    if _match:
        return _match.group(index)