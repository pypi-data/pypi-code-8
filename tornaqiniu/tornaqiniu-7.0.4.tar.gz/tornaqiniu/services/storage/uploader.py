# -*- coding: utf-8 -*-

import os
import tornado.gen

from tornaqiniu import config
from tornaqiniu.utils import urlsafe_base64_encode, crc32, file_crc32, _file_iter
from tornaqiniu import http

@tornado.gen.engine
def put_data(
        up_token, key, data, params=None, mime_type='application/octet-stream', check_crc=False, progress_handler=None, callback=None):
    """上传二进制流到七牛

    Args:
        up_token:         上传凭证
        key:              上传文件名
        data:             上传二进制流
        params:           自定义变量，规格参考 http://developer.qiniu.com/docs/v6/api/overview/up/response/vars.html#xvar
        mime_type:        上传数据的mimeType
        check_crc:        是否校验crc32
        progress_handler: 上传进度

    Returns:
        一个dict变量，类似 {"hash": "<Hash string>", "key": "<Key string>"}
        一个ReponseInfo对象
    """
    crc = crc32(data) if check_crc else None
    _form_put(up_token, key, data, params, mime_type, crc, False, progress_handler,callback=callback)

@tornado.gen.engine
def put_file(up_token, key, file_path, params=None, mime_type='application/octet-stream', check_crc=False, progress_handler=None, callback=None):
    """上传文件到七牛

    Args:
        up_token:         上传凭证
        key:              上传文件名
        file_path:        上传文件的路径
        params:           自定义变量，规格参考 http://developer.qiniu.com/docs/v6/api/overview/up/response/vars.html#xvar
        mime_type:        上传数据的mimeType
        check_crc:        是否校验crc32
        progress_handler: 上传进度

    Returns:
        一个dict变量，类似 {"hash": "<Hash string>", "key": "<Key string>"}
        一个ReponseInfo对象
    """
    ret = {}
    size = os.stat(file_path).st_size
    with open(file_path, 'rb') as input_stream:
        if size > config._BLOCK_SIZE * 2:
            ret, info = yield tornado.gen.Task(put_stream, up_token, key, input_stream, size, params, mime_type, progress_handler)
        else:
            crc = file_crc32(file_path) if check_crc else None
            ret, info = yield tornado.gen.Task(_form_put, up_token, key, input_stream, params, mime_type, crc, True, progress_handler)
    callback(( ret, info ))

@tornado.gen.engine
def _form_put(up_token, key, data, params, mime_type, crc, is_file=False, progress_handler=None, callback=None):
    fields = {}
    if params:
        for k, v in params.items():
            fields[k] = str(v)
    if crc:
        fields['crc32'] = crc
    if key is not None:
        fields['key'] = key
    fields['token'] = up_token
    url = 'http://' + config.get_default('default_up_host') + '/'
    name = key if key else 'filename'

    r, info = yield tornado.gen.Task(http._post_file,url, data=fields, files={'file': (name, data, mime_type)})
    if r is None and info.need_retry():
        if info.connect_failed:
            url = 'http://' + config.UPBACKUP_HOST + '/'
        if is_file:
            data.seek(0)
        r, info = yield tornado.gen.Task(http._post_file,url, data=fields, files={'file': (name, data, mime_type)})

    callback(( r,info ))

@tornado.gen.engine
def put_stream(up_token, key, input_stream, data_size, params=None, mime_type=None, progress_handler=None, callback=None):
    task = _Resume(up_token, key, input_stream, data_size, params, mime_type, progress_handler)
    task.upload(callback)


class _Resume(object):
    """断点续上传类

    该类主要实现了断点续上传中的分块上传，以及相应地创建块和创建文件过程，详细规格参考：
    http://developer.qiniu.com/docs/v6/api/reference/up/mkblk.html
    http://developer.qiniu.com/docs/v6/api/reference/up/mkfile.html

    Attributes:
        up_token:         上传凭证
        key:              上传文件名
        input_stream:     上传二进制流
        data_size:        上传流大小
        params:           自定义变量，规格参考 http://developer.qiniu.com/docs/v6/api/overview/up/response/vars.html#xvar
        mime_type:        上传数据的mimeType
        progress_handler: 上传进度
    """

    def __init__(self, up_token, key, input_stream, data_size, params, mime_type, progress_handler):
        """初始化断点续上传"""
        self.up_token = up_token
        self.key = key
        self.input_stream = input_stream
        self.size = data_size
        self.params = params
        self.mime_type = mime_type
        self.progress_handler = progress_handler

    @tornado.gen.engine
    def upload(self, callback=None):
        """上传操作"""
        self.blockStatus = []
        host = config.get_default('default_up_host')
        for block in _file_iter(self.input_stream, config._BLOCK_SIZE):
            length = len(block)
            crc = crc32(block)
            ret, info = yield tornado.gen.Task(self.make_block, block, length, host)

            if ret is None and not info.need_retry:
                callback( (ret,info) )
                return
            if info.connect_failed:
                host = config.UPBACKUP_HOST
            if info.need_retry or crc != ret['crc32']:
                ret, info = yield tornado.gen.Task(self.make_block, block, length, host)
                if ret is None or crc != ret['crc32']:
                    callback( (ret,info) )
                    return

            self.blockStatus.append(ret)
            if(callable(self.progress_handler)):
                self.progress_handler(((len(self.blockStatus) - 1) * config._BLOCK_SIZE)+length, self.size)
        self.make_file(host, callback=callback)

    @tornado.gen.engine
    def make_block(self, block, block_size, host, callback=None):
        """创建块"""
        url = self.block_url(host, block_size)
        self.post(url, block, callback=callback)

    def block_url(self, host, size):
        return 'http://{0}/mkblk/{1}'.format(host, size)

    def file_url(self, host):
        url = ['http://{0}/mkfile/{1}'.format(host, self.size)]

        if self.mime_type:
            url.append('mimeType/{0}'.format(urlsafe_base64_encode(self.mime_type)))

        if self.key is not None:
            url.append('key/{0}'.format(urlsafe_base64_encode(self.key)))

        if self.params:
            for k, v in self.params.items():
                url.append('{0}/{1}'.format(k, urlsafe_base64_encode(v)))

        url = '/'.join(url)
        return url

    def make_file(self, host, callback=None):
        """创建文件"""
        url = self.file_url(host)
        body = ','.join([status['ctx'] for status in self.blockStatus])
        self.post(url, body, callback=callback)

    @tornado.gen.engine
    def post(self, url, data, callback=None):
        http._post_with_token(url, data, self.up_token, callback=callback)
