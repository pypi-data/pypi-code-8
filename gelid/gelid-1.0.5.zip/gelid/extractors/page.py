# -*- coding: UTF-8 -*-
# lvjiyong on 2015/4/19.
from gelid.extractors import html
from gelid.extractors.decorator import store, inner


class Page(object):
    """页面HTML片断存储"""
    def __init__(self, source, url=None):
        self.url = url
        self.stores = {'html': source}

    @property
    @store
    def html(self):
        return None

    @property
    @store
    @inner
    def header(self):
        return None

    @property
    @store
    @inner
    def body(self):
        return None

    @property
    @store
    @inner
    def title(self):
        return None

    @property
    @store
    def html_clean(self):
        return html.set_html_clean(self.html)

    @property
    @store
    def txt(self):
        return html.txt(self.html_clean)

