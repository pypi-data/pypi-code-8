#coding=utf-8

from urllib import unquote_plus

def get_parameter(request, pname, default=None):
    """
    - 从request中获取参数
    - get_parameter(request, 'name', 'hello') => 获取参数name的值，不存在则为'hello'
    """
    v = request.REQUEST.get(pname, default).strip()
    return unquote_plus(v)