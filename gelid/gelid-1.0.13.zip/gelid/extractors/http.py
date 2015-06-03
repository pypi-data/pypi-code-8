# -*- coding: UTF-8 -*-
# lvjiyong on 2015/4/20.

"""

本文件中的方法仅为测试提供服务，gelid只专注于文本内容分析。

"""

import urllib2
from StringIO import StringIO
import gzip
from urlparse import urljoin, urlparse
import chardet
from gelid.extractors.log import logger
from gelid.extractors import regex


class Request(object):
    """
    封装http请求，输出response等
    """
    def set_response(self, url, timeout=30):

        headers = dict()
        self.url = url
        if url and str(url).startswith('http'):
            html, headers = Http.get_unicode_with_header(url, count=self.count, data=self.data, headers=self.headers)
            self._body = html
        self.response = Response(url=url,
                                 method=self.method,
                                 headers=headers,
                                 body=self._body,
                                 cookies=headers.get('Cookie'),
                                 meta=self.meta, encoding=self._encoding)

        # 获取编码方式并解码
        if url:
            if not self._encoding:
                self._encoding = regex.match_encoding(self._body)
                if not self._encoding:
                    self._encoding = regex.match_encoding(headers.get("Content-Type", ""))
                if not self._encoding:
                    self._encoding = 'utf-8'

            self.response.encoding = self._encoding
            if self._encoding.lower() in ('gbk', 'gb2312'):
                self._encoding = 'gb18030'
            try:
                self.response._body_as_unicode = self._body.decode(self._encoding, 'ignore')
            except Exception as e:
                logger.debug(e)
                encode = chardet.detect(self._body)
                self.response.encoding = self._encoding = encode.get('encoding')
                self.response._body_as_unicode = self._body.decode(self._encoding, 'ignore')

    def __init__(self, url, callback=None, method='GET', headers=None, body=None,
                 cookies=None, meta=None, encoding=None, err_callback=None, data=None, timeout=30):
        self._encoding = encoding
        self.method = str(method).upper()
        self.url = url
        self.body = body
        self.callback = callback
        self.err_callback = err_callback
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
            if err_callback:
                err_callback(e)
            else:
                raise e


class Http(object):
    @staticmethod
    def headers(url='', cookie=''):
        """
        初使化请求header
        :param url:
        :param cookie:
        :return:
        """
        _url = urlparse(url)
        header_dict = dict()
        header_dict['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:34.0) Gecko/20100101 Firefox/34.0'
        header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        header_dict['Accept-Language'] = 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3'
        header_dict['Referer'] = "http://{0}{1}".format(_url.hostname, _url.path)
        header_dict['Accept-Encoding'] = 'gzip, deflate'
        if cookie and len(cookie) > 0:
            header_dict['Cookie'] = cookie
        return header_dict

    @staticmethod
    def get_unicode_with_header(url, headers=None, no_redirect=None, count=0, data=None, timeout=30, error_callback=None):
        """
        获取请求内容，返回内容与header
        :param url:
        :param headers:
        :param no_redirect:
        :param count:
        :param data:
        :param timeout:
        :return:
        """
        html = None
        if not headers:
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
            # 如果有跳转，则进行跳转
            if not no_redirect and count < 2:
                if page.getcode() in [301, 302, 303, 307] and 'Location' in page.headers:
                    redirected_url = urljoin(url, page.headers['location'])
                    return Http.get_unicode(redirected_url, headers=headers, no_redirect=no_redirect,
                                            count=count + 1)
            headers = page.headers
            page.close()
        except Exception as e:
            if error_callback:
                error_callback(e)
            logger.debug(e)
        return html, headers

    @staticmethod
    def get_unicode(url, headers=None, no_redirect=None, count=0, data=None, timeout=30, error_callback=None):
        """
        获取网页内容
        :param url:
        :param headers:
        :param no_redirect:
        :param count:
        :param data:
        :param timeout:
        :param error_callback:
        :return:
        """
        html, headers = Http.get_unicode_with_header(url=url, headers=headers, no_redirect=no_redirect, count=count,
                                                     data=data, timeout=timeout, error_callback=error_callback)
        return html

    @staticmethod
    def get_file(url, headers=None, error_callback=None):
        """
        获取内容，只下载header中的Content-Type有image或stream标记的
        """
        download = None
        try:
            if not headers:
                headers = Http.headers(url)

            if url and str(url).startswith('http'):
                req = urllib2.Request(url=url, headers=headers)
                page = urllib2.urlopen(req, timeout=30)
                server_headers = page.headers
                name = 'Content-Type'
                if name in server_headers and ('image' in server_headers[name] or 'stream' in server_headers[name]):
                    download = page.read()
                page.close()
        except Exception as e:
            if error_callback:
                error_callback(e)
            logger.debug(e)
        return download


class Response(object):
    """
    封装输出
    """
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