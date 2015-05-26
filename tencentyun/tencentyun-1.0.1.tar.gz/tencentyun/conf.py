# -*- coding: utf-8 -*-
import pkg_resources
import platform

API_IMAGE_END_POINT = 'http://web.image.myqcloud.com/photos/v1/'
APPID = '您的APPID'
SECRET_ID = '您的SECRETID'
SECRET_KEY = '您的SECRETKEY'

_config = {
    'end_point':API_IMAGE_END_POINT,
    'appid':APPID,
    'secret_id':SECRET_ID,
    'secret_key':SECRET_KEY,
}

def get_app_info(cate='image'):
    if 'image' == cate:
        return _config
    else:
        return _config

def set_app_info(appid=None,secret_id=None,secret_key=None):
    if appid:
        _config['appid'] = appid
    if secret_id:
        _config['secret_id'] = secret_id
    if secret_key:
        _config['secret_key'] = secret_key

def get_ua():
    version = pkg_resources.require("tencentyun")[0].version
    return 'QcloudPYTHON/'+version+' ('+platform.platform()+')';


