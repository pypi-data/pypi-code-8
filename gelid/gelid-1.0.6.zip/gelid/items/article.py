# -*- coding: UTF-8 -*-
# lvjiyong on 2015/4/19.
from gelid.extractors import title, content, scan, timee

from gelid.extractors.page import Page, store, html


class Article(object):
    def __init__(self, source, url=None):
        self.page = Page(source=source, url=url)
        self.stores = {}

    @property
    @store
    def next_page(self):
        return html.next_page(self.page.url, self.page.html_clean)

    @property
    @store
    def title(self):
        """
        基于title文本扫描分析标题
        :return:
        """
        return title.title_in_content(self.page.title, self.page.body)

    @property
    @store
    def content(self):
        return content.rank_content(self.page.html_clean, clear=True)

    @property
    @store
    def author(self):
        return scan.get_author(self.page.txt)

    @property
    @store
    def time_posted(self):
        return timee.get_timestamp(scan.get_time(self.page.txt))

    @property
    @store
    def come_from(self):
        return scan.get_from(self.page.txt)