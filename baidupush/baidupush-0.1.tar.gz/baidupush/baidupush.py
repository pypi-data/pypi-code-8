#!/usr/bin/python
# coding=utf-8

"""
  百度云推送服务端SDK Python版本
  @version 1.0.0
"""

import time
import urllib
import hashlib

try:
    # ujson is faster than normal json
    from ujson import dumps
except ImportError:
    from json import dumps
import requests

class BaiduPushError(Exception):
    pass


class BaiduPush(object):
    """
    BaiduPush类提供百度云推送服务端SDK的Python版本，
    用户首先实例化这个类，设置自己的apikey和secretkey，即可使用Push服务接口
    """
    # 用户发起请求时的unix时间戳。本次请求签名的有效时间为该时间戳+10分钟
    TIMESTAMP = 'timestamp'

    # 用户指定本次请求签名的失效时间。格式为unix时间戳形式
    EXPIRES = 'expires'

    # API版本号，默认使用最高版本
    VERSION = 'v'

    # 通道标识
    CHANNEL_ID = 'channel_id'

    # 用户标识
    USER_ID = 'user_id'

    # 设备类型。如果存在此字段，则只返回该设备类型的绑定关系；默认不区分设备类型
    DEVICE_TYPE = 'device_type'

    # 可选设备类型
    DEVICE_BROWSER = 1
    DEVICE_PC = 2
    DEVICE_ANDRIOD = 3
    DEVICE_IOS = 4
    DEVICE_WINDOWSPHONE = 5

    # 查询起始页码，默认为0
    START = 'start'

    # 一次查询条数，默认为10
    LIMIT = 'limit'

    # 指定消息内容，单个消息为单独字符串
    MESSAGES = 'messages'

    # 删除的消息id列表，由一个或多个msg_id组成，多个用json数组表示
    MSG_IDS = 'msg_ids'

    # 消息标识。指定消息标识，自动覆盖相同消息标识的消息，只支持android、browser、pc三种设备类型。
    MSG_KEYS = 'msg_keys'

    # 消息类型，0:消息（透传），1:通知，默认为0
    MESSAGE_TYPE = 'message_type'

    # 可选消息类型
    PUSH_MESSAGE = 0
    PUSH_NOTIFICATION = 1

    # 指定消息的过期时间，默认为86400秒。
    MESSAGE_EXPIRES = 'message_expires'

    # 标签名，可按标签分组
    TAG_NAME = 'tag'

    # 标签信息
    TAG_INFO = 'info'

    # 标签ID
    TAG_ID = 'tid'

    # 访问令牌，明文AK，可从此值获得App的信息，配合sign中的sk做合法性身份认证。
    API_KEY = 'apikey'

    # 开发者密钥，用于调用HTTP API时进行签名加密，以证明开发者的合法身份。
    SECRET_KEY = 'secret_key'

    # Channel常量
    SIGN = 'sign'
    METHOD = 'method'
    HOST = 'host'
    PRODUCT = 'channel'
    DEFAULT_HOST = 'channel.api.duapp.com'

    # 证书相关常量
    NAME = 'name'
    DESCRIPTION = 'description'
    CERT = 'cert'
    RELEASE_CERT = 'release_cert'
    DEV_CERT = 'dev_cert'

    # 推送类型
    PUSH_TYPE = 'push_type'

    # 可选推送类型
    PUSH_TO_USER = 1
    PUSH_TO_TAG = 2
    PUSH_TO_ALL = 3

    # Channel错误常量
    CHANNEL_SDK_SYS = 1
    CHANNEL_SDK_INIT_FAIL = 2
    CHANNEL_SDK_PARAM = 3
    CHANNEL_SDK_HTTP_STATUS_ERROR_AND_RESULT_ERROR = 4
    CHANNEL_SDK_HTTP_STATUS_OK_BUT_RESULT_ERROR = 5

    _METHOD_CHANNEL_IN_BODY = ('push_msg', 'set_tag', 'fetch_tag', \
                                'delete_tag', 'query_user_tags')

    ###
    # 对外接口
    ###

    def __init__(self, apikey, secretkey):
        self._apikey = apikey
        self._secretkey = secretkey
        self.request_id = 0

    @property
    def apikey(self):
        return self._apikey

    @apikey.setter
    def apikey(self, value):
        self._apikey = value

    @property
    def secrectkey(self):
        return self._secretkey

    @secrectkey.setter
    def secrectkey(self, value):
        self._secretkey = value

    def get_requestid(self):
        return self.request_id

    def query_bindlist(self, user_id, optional=None):
        """
        描述:
            查询设备、应用、用户与百度Channel的绑定关系
        参数:
            str user_id:用户ID号
            dict optional:可选参数
        返回值:
            成功:python字典；失败:False
        """
        tmp_args = [user_id, optional]
        arr_args = self._merge_args([self.USER_ID], tmp_args)
        arr_args[self.METHOD] = 'query_bindlist'
        return self._common_process(arr_args)

    def push_msg(self, push_type, messages, message_keys, optional=None):
        """
        描述:
            推送消息，该接口可用于推送单个人、一群人、
            所有人以及固定设备的使用场景
        参数:
            push_type:推送消息的类型
            messages:消息内容
            message_keys:消息key
            optional:可选参数
        返回值:
            成功:python字典；失败:False
        """
        tmp_args = [push_type, messages, message_keys, optional]
        arr_args = self._merge_args([self.PUSH_TYPE, self.MESSAGES, \
                                    self.MSG_KEYS], tmp_args)
        arr_args[self.METHOD] = 'push_msg'
        arr_args[self.PUSH_TYPE] = push_type
        arr_args[self.MESSAGES] = dumps(arr_args[self.MESSAGES])
        arr_args[self.MSG_KEYS] = dumps(arr_args[self.MSG_KEYS])
        return self._common_process(arr_args)

    def verify_bind(self, user_id, optional=None):
        """
        描述:
            判断设备、应用、用户与Channel的绑定关系是否存在
        参数:
            user_id:用户id
            optional:可选参数
        返回值:
            成功:python数组；失败:False
        """
        tmp_args = [user_id, optional]
        arr_args = self._merge_args([self.USER_ID], tmp_args)
        arr_args[self.METHOD] = 'verify_bind'
        return self._common_process(arr_args)

    def fetch_msg(self, user_id, optional=None):
        """
        描述:
            查询离线消息
        参数:
            user_id:用户id
            optional:可选参数
        返回值:
            成功:python字典；失败:False
        """
        tmp_args = [user_id, optional]
        arr_args = self._merge_args([self.USER_ID], tmp_args)
        arr_args[self.METHOD] = 'fetch_msg'
        return self._common_process(arr_args)

    def fetch_msgcount(self, user_id, optional=None):
        """
        描述:
            查询离线消息的个数
        参数:
            user_id:用户id
            optional:可选参数
        返回值:
            成功:python字典；失败:False
        """
        tmp_args = [user_id, optional]
        arr_args = self._merge_args([self.USER_ID], tmp_args)
        arr_args[self.METHOD] = 'fetch_msgcount'
        return self._common_process(arr_args)

    def delete_msg(self, user_id, msg_id, optional=None):
        """
        描述:
            删除离线消息
        参数:
            user_id:用户id
            msgIds:消息id
            optional:可选参数
        返回值:
            成功:python字典；失败:False
        """
        tmp_args = [user_id, msg_id, optional]
        arr_args = self._merge_args([self.USER_ID, self.MSG_IDS], tmp_args)
        arr_args[self.METHOD] = 'delete_msg'
        if isinstance(arr_args[self.MSG_IDS], list):
            arr_args[self.MSG_IDS] = dumps(arr_args[self.MSG_IDS])
        return self._common_process(arr_args)

    def set_tag(self, tag_name, optional=None):
        """
        描述:
            服务器端设置用户标签。
            当该标签不存在时，服务端将会创建该标签。
            特别地，当user_id被提交时，服务端将会完成用户和tag的绑定操作。
        参数:
            tag_name:标签
            optional:可选参数
        返回值:
            成功:python字典；失败:False
        """
        tmp_args = [tag_name, optional]
        arr_args = self._merge_args([self.TAG_NAME], tmp_args)
        arr_args[self.METHOD] = 'set_tag'
        return self._common_process(arr_args)

    def fetch_tag(self, optional=None):
        """
        描述:
            App Server查询应用标签
        参数:
            optional:可选参数
        返回值:
            成功:python字典；失败:False
        """
        tmp_args = [optional]
        arr_args = self._merge_args([], tmp_args)
        arr_args[self.METHOD] = 'fetch_tag'
        return self._common_process(arr_args)

    def delete_tag(self, tag_name, optional=None):
        """
        描述:
            服务端删除用户标签。
            特别地，当user_id被提交时，服务端将只会完成解除该用户与tag绑定关系的操作
            注意:该操作不可恢复，请谨慎使用。
        参数:
            tag_name:标签
            optional:可选参数
        返回值:
            成功:python字典；失败:False
        """
        tmp_args = [tag_name, optional]
        arr_args = self._merge_args([self.TAG_NAME], tmp_args)
        arr_args[self.METHOD] = 'delete_tag'
        return self._common_process(arr_args)

    def query_user_tag(self, user_id, optional=None):
        """
        描述:
            App Server查询用户所属的标签列表
        参数:
            user_id:用户id
            optional:可选参数
        返回值:
            成功:python字典；失败:False
        """
        tmp_args = [user_id, optional]
        arr_args = self._merge_args([self.USER_ID], tmp_args)
        arr_args[self.METHOD] = 'query_user_tags'
        return self._common_process(arr_args)

    def query_device_type(self, channel_id, optional=None):
        """
        描述:
            根据channel_id查询设备类型
        参数:
            ChannelId:用户Channel的ID号
            optional:可选参数
        返回值:
            成功:python字典；失败:False
        """
        tmp_args = [channel_id, optional]
        arr_args = self._merge_args([self.CHANNEL_ID], tmp_args)
        arr_args[self.METHOD] = 'query_device_type'
        return self._common_process(arr_args)


    ###
    # 内部函数
    ###

    def _adjust_opt(self, opt):
        if self.TIMESTAMP not in opt:
            opt[self.TIMESTAMP] = int(time.time())
        opt[self.HOST] = self.DEFAULT_HOST
        opt[self.API_KEY] = self._apikey
        if self.SECRET_KEY in opt:
            del opt[self.SECRET_KEY]

    def _gen_sign(self, method, url, arr_content):
        gather = method + url
        keys = arr_content.keys()
        keys.sort()
        for key in keys:
            gather += key + '=' + str(arr_content[key])
        gather += self._secretkey
        sign = hashlib.md5(urllib.quote_plus(gather))
        return sign.hexdigest()

    def _base_control(self, opt):
        resource = 'channel'
        if self.CHANNEL_ID in opt:
            if opt[self.CHANNEL_ID] and \
                    opt[self.METHOD] not in self._METHOD_CHANNEL_IN_BODY:
                resource = opt[self.CHANNEL_ID]
                del opt[self.CHANNEL_ID]

        host = opt[self.HOST]
        del opt[self.HOST]

        url = 'http://' + host + '/rest/2.0/' + self.PRODUCT + '/'
        url += resource
        http_method = 'POST'
        opt[self.SIGN] = self._gen_sign(http_method, url, opt)

        headers = dict()
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        headers['User-Agent'] = 'Baidu Channel Service Pythonsdk Client'

        return requests.post(url, data=opt, headers=headers)

    def _common_process(self, param_opt):
        self._adjust_opt(param_opt)
        ret = self._base_control(param_opt)
        result = ret.json()
        self.request_id = result['request_id']

        if ret.status_code == requests.codes.ok:
            return result
        raise BaiduPushError(result)

    def _merge_args(self, arr_need, tmp_args):
        arr_args = dict()

        if not arr_need and not tmp_args:
            return arr_args

        arr_need_len = len(arr_need)
        tmp_args_len = len(tmp_args)
        if tmp_args_len not in ( arr_need_len, arr_need_len + 1):
            keys = '('
            for key in arr_need:
                keys += key + ','
            if key[-1] == '' and key[-2] == ',':
                keys = keys[0:-2]
            keys += ')'
            raise BaiduPushError('invalid sdk, params, params' + keys + 'are need',
                    self.CHANNEL_SDK_PARAM)

        if tmp_args_len - 1 == arr_need_len and \
                tmp_args[-1] is not None and \
                not isinstance(tmp_args[-1], dict):
            raise BaiduPushError('invalid sdk params, '
                            'optional param must bean dict',
                            self.CHANNEL_SDK_PARAM)

        idx = 0
        if isinstance(arr_need, list):
            for key in arr_need:
                if tmp_args[idx] is None:
                    raise BaiduPushError('lack param ' + key,
                                         self.CHANNEL_SDK_PARAM)
                arr_args[key] = tmp_args[idx]
                idx = idx + 1

        if len(tmp_args) == idx + 1 and tmp_args[idx] is not None:
            for (key, value) in tmp_args[idx].items():
                if key not in arr_args and value is not None:
                    arr_args[key] = value

        return arr_args
