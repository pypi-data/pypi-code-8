# -*- coding: UTF-8 -*-
# lvjiyong on 2015/4/26.
import re
import jieba

from gelid.extractors import regex
from gelid.extractors import html
from gelid.extractors import score


def readability_content(source, only_content=True):
    """
    使用readability获取内容，需要安装 readability-lxml
    :param source:
    :param only_content:
    :return:
    """
    from readability.readability import Document

    doc = Document(source)
    if source and '<html>' in source:
        readable_article = doc.summary(html_partial=True)
        if readable_article and only_content:
            readable_article = regex.replace('<h1>.*?</h1>', '', readable_article)
        return readable_article


def distance_content(source, clear=False, article=False, duplicate=False):
    """
    根据行距离及距离中心距离实现主内容计算
    :param source:
    :return:
    """
    if not clear:
        source = html.set_html_clean(source)
    if not article:
        article_content = html.inner_text('article', source)
        if article_content:
            source = article_content
    pattern = '<div[^>]*>\s*</div>'
    body = regex.replace(pattern, '', source)
    # 过滤所有正文可能使用的标签
    tags = r'(?P<tag>/?(p|strong|img|font|span|br|h\d|a|b|i|u|pre|center)[\w\W]*?)'

    def holder_tags(content, tag):
        """
        变化指定标签
        :param content:
        :param tag:
        :return:
        """
        content = regex.replace('<{0}>'.format(tag), r'##\g<tag>##', content)
        # 转换\n为特殊符号┠
        return regex.replace(r'\n', u'┠', content)

    def clear_tags(content, tag):
        """
        清除转化标签
        :param content:
        :param tag:
        :return:
        """
        _pattern = re.compile(r'(##a [\w\W]*?##/a##)|(##{0}##)'.format(tag) + u'|(┠)', re.I)
        content = re.sub(_pattern, r"", content)
        tag = u'[^\u4e00-\u9fa5\ufe30-\uffa0]'
        return regex.replace(tag, u"", content)

    def recover(content, tag):
        """
        还原转化标签
        :param content:
        :param tag:
        :return:
        """
        _pattern = re.compile(r'##{0}##'.format(tag), re.I)
        return re.sub(_pattern, r'<\g<tag>>', content)

    body = holder_tags(body, tags)

    # 其它html标签转换行
    body = regex.replace(r'(</?.*?>)', r'\n', body)
    # 分割内容至数据
    lines = re.split(r'\n', body)
    # 清除保留的标签，以备文字计数
    z = [clear_tags(i, tags) for i in lines]

    def duplicate_line(line):
        tokens = jieba.cut(line)
        tokens = [token for token in tokens]
        tokens = set(tokens)
        line = ''.join(tokens)
        return line

    # 内容分词处理，清除重复词后再计算文字
    if duplicate:
        z = map(duplicate_line, z)

    # 计算行内数据长
    x = [len(i) for i in z]
    max_x = max(x)
    body = lines[x.index(max_x)]

    index = 0
    if max_x > 100 and index == 0:
        index = max_x
        # print(maxX)
    # 如果字数少于100字，则根据距离中心点重新计算
    if max_x < 100:
        mid = len(x) / 2
        if index > 0:
            mid = index
        t = []
        i = 0
        for count in x:
            abs_distance = abs(mid - i)
            nx = count * mid / ((abs_distance + mid) + 1)
            t.append(nx)
            i += 1
        body = lines[t.index(max(t))]

    body = recover(body, tags)
    # 替换原始┠为\n
    body = re.sub(u'┠', r'\n', body)
    # 所有标签改小写
    body = re.sub(r'<.*?>', lambda a: a.group().lower(), body)
    return body


def rank_content(source, clear=False, duplicate=True):
    # articles = list()
    # articles.append(dict(content=distance_content(source, duplicate=True)))
    # articles.append(dict(content=readability_content(source)))
    # score.rank(articles)[0][0]['content']
    distance_rank = score.Score(dict(content=distance_content(source, clear=clear, duplicate=False)))
    readability_rank = score.Score(dict(content=readability_content(source)))
    if distance_rank.rank + 5 > readability_rank.rank:
        return distance_rank.article['content']
    else:
        return readability_rank.article['content']

