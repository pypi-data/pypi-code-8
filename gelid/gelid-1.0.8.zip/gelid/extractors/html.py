# -*- coding: UTF-8 -*-
# lvjiyong on 2015/4/19.
import re
from urlparse import urlparse, urljoin
import six
from gelid.extractors import regex


def inner_text(tag, source):
    """返回标签内内容"""
    if tag and source:
        pattern = re.compile('<{0}.*?>([\w\W]+)</{0}>'.format(tag), re.I | re.M)
        search = re.search(pattern, source)
        if search:
            return search.group(1)


def urls(url):
    """
    返回urls字典
    """
    assert url, 'url不能为空'
    parse = urlparse(url)
    question_index = url.find('?')
    url_host = parse.hostname
    url_without_question = url if question_index == -1 else url[0:question_index]
    url_root = url_without_question[0:url_without_question.rfind('/') + 1]
    url_filename = url_without_question[url_without_question.rfind('/') + 1:]
    path_index = url_filename.find('.')
    fileid = url_filename if path_index == -1 else url_filename[0:path_index]
    pattern = re.compile(r"^(.+)[\-_]\d{1,2}$", re.I)
    match = re.search(pattern, fileid)
    if match:
        fileid = match.group(1)
    _urls = {"dir": url_root, "filename": url_filename, "fileid": fileid, 'domain': url_host}
    return _urls


def next_page(url, source, token=u'下一页|下页|&gt;|》|next|翻页|next page'):
    u"""自动分析下一页地址：
    假设分页都是类似的，均与当前URL有一定的规则关联，仅为分页码不一样或有无
    正则获取下一页地址，如果为找到分页，且分页地址符合规则，则为分页
    """
    if not url or not re.match(r'http.+', url):
        raise ValueError(u'url格式错误!')
    _urls = urls(url)
    fileid = _urls["fileid"]

    pattern = 'href=.*?' + fileid + '[\w\W]{1,200}?</a>'
    m = regex.find_all(pattern, source)
    page_url = None
    if m:
        for mc in m:
            if re.search(token, mc):
                pattern = r'href=\s*[\'"]([^\'"]*?' + fileid + r'[/\-\._][^\'" ]*?)[\'"]'
                mx = re.search(pattern, mc)
                if mx:
                    page_url = mx.group(1)
                    break
                else:
                    pattern = r'href=\s*([^\'"]*?' + fileid + r'[/\-\._][^\'"\s>]*)'
                    mx = re.search(pattern, mc)
                    if mx:
                        page_url = mx.group(1)
                        break

    if page_url:
        page_url = urljoin(url, page_url)
    return page_url


def clear_tags_with_content(tags, content):
    """清除标签组及中间的内容"""
    if isinstance(tags, six.string_types):
        tags = [tags]
    content = reduce(lambda x, y: clear_tag_with_content(y, x), tags, content)
    return content


def clear_tag_with_content(tag, content):
    """清除标签及中间的内容"""
    pattern = '<({0})[\w\W]*?>[\w\W]*?</\\1>'.format(tag)
    return regex.replace(pattern, '', content)


def clear_tags(tags, content):
    """清除标签组"""
    if isinstance(tags, six.string_types):
        tags = [tags]
    content = reduce(lambda x, y: clear_tag(y, x), tags, content)
    return content


def clear_tag(tag, content):
    """清除标签"""
    pattern = '</?{0}.*?>'.format(tag)
    return regex.replace(pattern, '', content)


def txt(content):
    """生成txt，并返回txt"""
    pattern = '<[^>]*>|\r|\n|\t'
    content = regex.replace(pattern, '', content)
    pattern = "&nbsp;"
    content = regex.replace(pattern, ' ', content)
    pattern = "&[\w\d]{2,8}?;"
    content = regex.replace(pattern, '', content)
    return content


def clear_comment(content):
    """清除注释"""
    pattern = '<!--[\w\W]+?-->'
    return regex.replace(pattern, '', content)


def set_html_clean(content):
    """生成html无用标签清洗后的内容"""
    tags = ['script', 'style', 'head']
    content = clear_comment(content)
    content = clear_tags_with_content(tags, content)
    return content


def http_join(url, content, tags='a|img', attrs='src|href', protocol='http|ftp'):
    """
    将内容中指定位置的url转为http开头的绝对路径
    根据items指定的参数，结合html结构抽取分别属性由双引号，单引号，后空格等形式的链接保存至字典
    遍历字典替换文本中的url为http url
    """
    # print(tags)
    # print(attrs)
    pattern = "(<({0}) [^>]*?({1})[\s=]*[\"']?([^>]*?)[\"' >])".format(tags, attrs)
    print(pattern)
    findall = regex.find_all(pattern, content)
    match_dict = dict()
    for match in findall:
        # print(match)
        print(match[0])
        match_dict[match[0]] = match[3]
    _protocol = protocol.split('|')

    def __is_not_full(i, p):
        for _p in p:
            if str(i).startswith(_p):
                return True
        return False

    for k, v in match_dict.iteritems():
        if not __is_not_full(v, _protocol):
            http_k = urljoin(url, v)
            v2 = k.replace(v, http_k)
            content = content.replace(k, v2)
    return content


def rebuild_url(content, url):
    return http_join(url, content)


def rebuild_img(content):
    return regex.replace("<img[\w\W]*?src=['\"](.*?\.jpg)['\"][\w\W]*?>", '<img src="\g<1>" class="img-responsive">',
                         content)


def images(content):
    pattern = '<img.*?src=["](.*?\.jpg)["].*?>'
    return regex.find_all(pattern, content)


def rebuild(content, url):
    return rebuild_img(rebuild_url(content, url))

