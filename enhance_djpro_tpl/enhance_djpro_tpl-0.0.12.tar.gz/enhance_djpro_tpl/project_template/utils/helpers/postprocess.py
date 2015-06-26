#coding=utf-8
#
import json
from django.http import HttpResponse

def _response_as_json(request, obj):
    """
    - 将一个Py对象转成JSON，构造返回HttpResponse
    - _response_as_json(request, {'data':'test'}) => HttpResponse
    """
    response = HttpResponse(mimetype="application/json")
    res = json.dumps(obj)
    response.write(res)
    response['Access-Control-Allow-Origin'] = '*'
    return response