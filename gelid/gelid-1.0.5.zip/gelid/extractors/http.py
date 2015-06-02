# -*- coding: UTF-8 -*-
# lvjiyong on 2015/4/20.

"""

本文件中的方法仅为测试提供服务，gelid只专注于文本内容分析。

"""

import urllib2
from StringIO import StringIO
import gzip
from urlparse import urljoin

from gelid.extractors import regex


class Request(object):
    """
    Hello Request
    """

    def set_response(self, url, timeout=30):

        self.url = url
        if url:
            self._body = Http.get_unicode(url, count=self.count, data=self.data, headers=self.headers, timeout=timeout)

        self.response = Response(url=url,
                                 method=self.method,
                                 # headers=self.headers,
                                 body=self._body,
                                 cookies=self.cookies,
                                 meta=self.meta, encoding=self._encoding)

        if url:
            if not self._encoding:
                self._encoding = regex.match_encoding(self._body)
                if not self._encoding:
                    self._encoding = 'utf-8'
            self.response.encoding = self._encoding
            if self._encoding.lower() in ('gb2312', 'gbk'):
                self._encoding = 'gb18030'
            self.response._body_as_unicode = self._body.decode(self._encoding)

    def __init__(self, url, callback=None, method='GET', headers=None, body=None,
                 cookies=None, meta=None, encoding=None, errback=None, data=None, timeout=30):
        self._encoding = encoding
        self.method = str(method).upper()
        self.url = url
        self.body = body
        self.callback = callback
        self.errback = errback
        self.cookies = cookies or {}
        self.headers = headers
        self.meta = dict(meta) if meta else None
        self._body = None
        self.response = None
        self.count = 0
        self.data = data
        try:
            self.set_response(url=url, timeout=timeout)
            if callback:
                call = callback(self.response)
                if hasattr(call, 'next'):
                    call.next()
        except Exception as e:
            if errback:
                errback(e)
            else:
                raise e


class Http(object):
    @staticmethod
    def headers(url='', cookie=''):
        return {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:34.0) Gecko/20100101 Firefox/34.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
            'Accept-Encoding': 'html',
            'Cookie': cookie,
            'Referer': url
        }

    @staticmethod
    def get_unicode(url, headers=None, dont_redirect=None, count=0, data=None, timeout=30):
        html = None
        if headers is None:
            headers = Http.headers(url)
        try:
            req = urllib2.Request(url=url, headers=headers, data=data)
            page = urllib2.urlopen(req, timeout=timeout)

            if page.info().get('Content-Encoding') == 'gzip':
                buf = StringIO(page.read())
                body = gzip.GzipFile(fileobj=buf)
                html = body.read()
            else:
                html = page.read()

            if not dont_redirect and count < 2:
                if page.getcode() in [301, 302, 303, 307] and 'Location' in page.headers:
                    redirected_url = urljoin(url, page.headers['location'])
                    return Http.get_unicode(redirected_url, headers=headers, dont_redirect=dont_redirect,
                                            count=count + 1)
            page.close()
        except Exception as e:
            print(e)
        return html

    @staticmethod
    def get_file(url, headers=None):
        download = None
        try:
            if headers is None:
                headers = Http.headers(url)

            if url and str(url).startswith('http'):
                req = urllib2.Request(url=url, headers=headers)
                page = urllib2.urlopen(req)
                download = page.read()
                page.close()
        except Exception as e:
            print(e)
        return download


class Response(object):
    def __init__(self, url, method='GET', headers=None, body=None,
                 cookies=None, meta=None, encoding='utf-8'):
        self.encoding = encoding
        self.body = body
        self.url = url
        self.meta = method
        self._body_as_unicode = None
        self.cookies = cookies or {}
        self.headers = headers or dict()
        self.meta = meta if meta else None
        self._cached_selector = None

    def body_as_unicode(self):
        return self._body_as_unicode