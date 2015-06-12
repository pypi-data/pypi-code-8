from django.db import connection
from django.utils.functional import lazy


def sql_queries_context(request):
    if request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS:
        return {
            'sql_queries': lazy(lambda: connection.queries, list)
        }


def show_toolbar(request):
    # TODO
    return True
