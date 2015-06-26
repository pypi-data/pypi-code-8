#coding=utf-8
#
from {{ project_name }}.settings import logger

def catch_exception(func):
    """
    - 视图函数异常错误处理装饰器
    """
    @functools.wraps(func)
    def newfunc(request):
        logger.exception(u'%s,参数:%s' % (request.get_full_path(), str(request.REQUEST)))
        try:
            back = func(request)
            return back
        except Exception, e:
            excep = u'异常:%s' % str(e)
            detail = u'跟踪:%s' % traceback.format_exc()
            logger.exception(excep)
            logger.exception(detail)
            return _response_as_json(request, {'code':500, 'msg':str(e)})
    return newfunc