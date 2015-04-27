# -*- coding: utf-8 -*-
import platform

import simplejson
import requests
import tornado.gen
from requests.auth import AuthBase

from tornaqiniu import config
from .auth import RequestsAuth
from .tornadohttpclient import TornadoHTTPClient
from . import __version__


_sys_info = '{0}; {1}'.format(platform.system(), platform.machine())
_python_ver = platform.python_version()

USER_AGENT = 'QiniuPython/{0} ({1}; ) Python/{2}'.format(__version__, _sys_info, _python_ver)

_http = None
_headers = {'User-Agent': USER_AGENT}


def __return_wrapper(resp):
    if resp.code != 200:
        return None, ResponseInfo(resp)
    ret = simplejson.loads(resp.body) if resp.body != '' else {}
    return ret, ResponseInfo(resp)


def _init():
    global _http
    _http = TornadoHTTPClient()
    _http.set_proxy(config.PROXY_HOST,config.PROXY_PORT)


@tornado.gen.engine
def _post(url, data, files, auth, callback=None):
    if _http is None:
        _init()
    try:
        r = yield tornado.gen.Task(_http.post,
            url, params=data, files=files, auth=auth, headers=_headers, connect_timeout=config.get_default('connection_timeout'))
    except Exception:
        import traceback
        print traceback.format_exc()
        callback( None, ResponseInfo(None, traceback.format_exc()) )
        return
    ret,info = __return_wrapper(r)
    callback((ret,info ))

@tornado.gen.engine
def _get(url, params, auth,callback=None):
    if _http is None:
        _init()
    try:
        r = yield tornado.gen.Task(_http.get,
            url, params=params, auth=RequestsAuth(auth) if auth is not None else None,
            connect_timeout=config.get_default('connection_timeout'), headers=_headers)
    except Exception:
        import traceback
        callback( None, ResponseInfo(None, traceback.format_exc()) )
        return
    ret,info = __return_wrapper(r)
    callback( ret,info )


class _TokenAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['Authorization'] = 'UpToken {0}'.format(self.token)
        return r

def _post_with_token(url, data, token, callback=None):
    _post(url, data, None, _TokenAuth(token), callback=callback)

def _post_file(url, data, files, callback=None):
    _post(url, data, files, None,callback=callback)

def _post_with_auth(url, data, auth, callback=None):
    _post(url, data, None, RequestsAuth(auth), callback=callback)


class ResponseInfo(object):
    """七牛HTTP请求返回信息类

    该类主要是用于获取和解析对七牛发起各种请求后的响应包的header和body。

    Attributes:
        status_code: 整数变量，响应状态码
        text_body:   字符串变量，响应的body
        req_id:      字符串变量，七牛HTTP扩展字段，参考 http://developer.qiniu.com/docs/v6/api/reference/extended-headers.html
        x_log:       字符串变量，七牛HTTP扩展字段，参考 http://developer.qiniu.com/docs/v6/api/reference/extended-headers.html
        error:       字符串变量，响应的错误内容
    """

    def __init__(self, response, exception=None):
        """用响应包和异常信息初始化ResponseInfo类"""
        self.__response = response
        self.exception = exception
        if response is None:
            self.status_code = -1
            self.text_body = None
            self.req_id = None
            self.x_log = None
            self.error = str(exception)
        else:
            self.status_code = response.code
            self.text_body = response.body
            self.req_id = response.headers['X-Reqid']
            self.x_log = response.headers['X-Log']
            if self.status_code >= 400:
                ret = simplejson.loads(response.body) if response.body != '' else None
                if ret is None or ret['error'] is None:
                    self.error = 'unknown'
                else:
                    self.error = ret['error']

    def ok(self):
        return self.status_code == 200

    def need_retry(self):
        if self.__response is None:
            return True
        code = self.status_code
        if (code // 100 == 5 and code != 579) or code == 996:
            return True
        return False

    def connect_failed(self):
        return self.__response is None

    def __str__(self):
        return ', '.join(['%s:%s' % item for item in self.__dict__.items()])

    def __repr__(self):
        return self.__str__()