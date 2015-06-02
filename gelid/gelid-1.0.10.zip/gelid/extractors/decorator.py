# -*- coding: UTF-8 -*-
# lvjiyong on 2015/4/25.

from gelid.extractors import html


def store(func):
    def modify(*args, **kwargs):
        page = args[0]
        key = func.__name__
        value = page.stores.get(key)
        if not value:
            value = func(*args, **kwargs)
            if not value:
                page.stores[key] = value
        return value
    return modify


def inner(func):
    def modify(*args, **kwargs):
        page = args[0]
        key = func.__name__
        return html.inner_text(key, page.html)
    return modify