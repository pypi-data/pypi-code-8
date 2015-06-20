# TODO Can we import settings here without causing circular import issues?


def has_magic(request):
    from django.conf import settings

    magic = getattr(settings, 'DEBUG_MAGIC', None)
    if magic and magic == request.GET.get('__magic', None):
        return True

    return False


def sql_queries_context(request):
    from django.conf import settings

    if settings.DEBUG and has_magic(request):
        from django.db import connection
        from django.utils.functional import lazy

        return {
           'sql_queries': lazy(lambda: connection.queries, list)
        }
    return {}


def show_toolbar(request):
    from django.conf import settings

    return settings.DEBUG and (getattr(settings, 'DEBUG_TOOLBAR', False) or has_magic(request))
