# -*- coding: UTF-8 -*-
# lvjiyong on 2015/6/7.

"""
简单装了python-gelid可能用到的http请求
request_with_header：带有较完整的http请求及返回
request：简单返回内容
request：简单返回可能是图片或文件的数据，如果不是则返回空
"""
import socket

__all__ = ['request_with_header', 'request', 'request_file']

from StringIO import StringIO
import gzip
import urllib2
from urlparse import urljoin
from ghttp import utils, settings
from ghttp.parameter import Parameter

_dns_cache = {}


def _set_dns_cache():
    def _getaddrinfo(*args, **kwargs):
        global _dns_cache
        if args in _dns_cache:
            return _dns_cache[args]
        else:
            _dns_cache[args] = socket._getaddrinfo(*args, **kwargs)
            return _dns_cache[args]

    if not hasattr(socket, '_getaddrinfo'):
        socket._getaddrinfo = socket.getaddrinfo
        socket.getaddrinfo = _getaddrinfo


def request_with_header(url, **kwargs):
    """
    获取请求内容，返回内容与header
    >>> page = request_with_header('https://www.baidu.com/')
    >>> 'baidu' in page[0]
    True
    >>> page[1].getcode()
    200
    >>> page[1].headers.get('Content-Encoding')
    'gzip'
    """
    params = Parameter(kwargs)
    max_request = params.max_request or 0
    timeout = params.timeout or settings.REQUEST_TIMEOUT
    auto_cookie_request = params.auto_cookie_request or False
    content = None
    page = Parameter()
    if not params.headers:
        params.headers = utils.http_headers(url)
    try:
        _set_dns_cache()
        if params.proxy:
            opener = urllib2.build_opener(urllib2.ProxyHandler(params.proxy))
            urllib2.install_opener(opener)

        req = urllib2.Request(url=url, headers=params.headers, data=params.data)
        page = urllib2.urlopen(req, timeout=timeout)
        # 如果gzip则解压缩
        if page.info().get('Content-Encoding') == 'gzip':
            buf = StringIO(page.read())
            body = gzip.GzipFile(fileobj=buf)
            content = body.read()
        else:
            content = page.read()
        # 如果有跳转且标识，则进行跳转
        if not params.no_redirect and max_request < 2:
            if page.getcode() in [301, 302, 303, 307] and 'Location' in page.headers:
                redirected_url = urljoin(url, page.headers['location'])
                params.max_request += 1
                return request_with_header(redirected_url, **params)
        page_headers = page.headers
        page.close()
        # 如果内容少于200字且标记为自动设置cookie重请求
        if len(content) < 200 and auto_cookie_request and max_request < 2:
            cookie_regex = utils.search_cookie(content)
            if cookie_regex:
                page_cookie = cookie_regex
            elif page_headers.get('Set-Cookie'):
                page_cookie = page_headers['Set-Cookie']
            else:
                page_cookie = None
            if page_cookie:
                params.headers['Cookie'] = page_cookie
                params.max_request += 1
                return request_with_header(url, **params)

    except Exception as e:
        if params.error_callback:
            params.error_callback(e)

    return content, page


def request(url, **kwargs):
    """
    获取网页内容
    >>> page = request('https://www.baidu.com/')
    >>> 'baidu' in page
    True
    """
    return request_with_header(url, **kwargs)[0]


def request_file(url, **kwargs):
    """
    获取内容，只下载header中的Content-Type有image或stream标记的
    >>> page = request_file('https://www.baidu.com/')
    >>> page

    >>> page = request_file('https://www.baidu.com/favicon.ico')
    >>> len(page) > 3000
    True
    """
    file_object = None
    error_callback = kwargs.get('error_callback')
    message = None
    if url and str(url).startswith('http'):
        http_request = request_with_header(url, **kwargs)
        if http_request[0]:
            content_type = http_request[1].headers.get('Content-Type')
            # 只获取文件头含有image或stream的内容
            if content_type and ('image' in content_type or 'stream' in content_type):
                file_object = http_request[0]
            else:
                message = 'Content-Type:%s' % message
    else:
        message = u'文件地址错误'
    if error_callback:
        error_callback(message)

    return file_object


if __name__ == "__main__":
    import doctest

    doctest.testmod()