# -*- coding: utf-8 -*-

__all__ = ['extract']


import re


def extract(pattern, data, fmt, multi=None):
    """
    格式化输出内容
    :param pattern: 匹配规则
    :param data: 原始数据
    :param fmt: 格式化输出$1,$2分别对应规则中捕获的组1，组2
    :return:
    >>> data = '12m34kjdg8946o'
    >>> pn = '(\d)([a-z])'
    >>> fm = '$1,$2'
    >>> result = extract(pn, data, fm)
    >>> result
    '2,m'
    >>> result = extract(pn, data, fm, multi= True)
    >>> result
    ['2,m', '4,k', '6,o']


    """
    pn = re.compile(pattern)

    fm_pn = re.compile(r'\$(\d+)')

    fm_finds = re.finditer(fm_pn, fmt)
    end = 0
    g = list()

    for i in fm_finds:
        i_start = i.start()
        i_end = i.end()
        if end < i_start:
            g.append(fmt[end:i_start])
        g.append(int(i.group(1)))
        end = i_end

    if end < len(fmt):
        g.append(fmt[end:len(fmt)])

    if multi is None or multi == 0:
        mc = re.search(pn, data)
        if mc:
            return _match_format(g, mc)
    else:
        m_finds = re.finditer(pn, data)
        mg = list()
        for m in m_finds:
            mg.append(_match_format(g, m))
        return mg


def _match_format(g, mc):
    gc = list()
    gc.extend(g)
    for i in range(0, len(gc)):
        j = gc[i]
        if isinstance(j, int):
            if j <= len(mc.groups()):
                gc[i] = mc.group(j)
            else:
                gc[i] = '$%s' % j
    return ''.join(gc)

if __name__ == "__main__":
    import doctest
    doctest.testmod()