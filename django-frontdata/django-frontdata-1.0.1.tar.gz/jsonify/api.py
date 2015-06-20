# encoding: utf-8

from collections import defaultdict


def has_frontdata(request):
    return hasattr(request, '_frontdata')


def get_frontdata(request):
    if not has_frontdata(request):
        request._frontdata = defaultdict(dict)
    return request._frontdata


def frontdata(request, key=None):
    return get_frontdata(request)[key or 'initial']
