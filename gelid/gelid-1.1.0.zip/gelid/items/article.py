# -*- coding: UTF-8 -*-
# lvjiyong on 2015/4/19.

from gelid.extractors import title, content as ex_content, scan, tm, regex, score
from gelid.extractors.page import Page, store, html
from gelidhttp import request
from gelid import settings


class Article(object):
    def __init__(self, source, url, keyword=None):
        self.page = Page(source=source, url=url)
        self.stores = {}
        self.keyword = keyword
        self.request_all = False

    def _request(self, url, contents, pages, contents_images):
        """
        获取分页内容
        :param url:
        :param contents:
        :param pages:
        :param contents_images:
        :return:
        """
        if not contents:
            contents = list()

        if not pages:
            pages = list()

        if url not in pages:
            source = request.Request(url=url).response.body_as_unicode()
            if source:
                article = Article(source, url)
                _content = article.content
                # 清除之前有的图片
                for image in contents_images:
                    _content = regex.replace('<img .*?src=[\'" ]*{0}[\'" ]*.*?>'.format(image), '', _content)

                for image in article.images:
                    if image not in contents_images:
                        contents_images.append(image)
                if _content not in contents:
                    contents.append(_content)
                    pages.append(url)
                    next_page = html.next_page(url, source)
                    if next_page:
                        self._request(next_page, contents, pages, contents_images)

        self.page.stores['images'] = contents_images
        return contents

    def _page_contents(self):
        """
        获取所有分页内容
        :return:
        """
        pages = [self.page.url]
        contents = [self.content]
        contents_images = self.images
        next_page = html.next_page(self.page.url, self.page.html_clean)
        if next_page:
            return self._request(next_page, contents, pages, contents_images)
        else:
            return contents

    @property
    @store
    def page_contents(self):
        """
        所有分页内容
        :return:
        """
        self.request_all = True
        return self._page_contents()

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
        print(self.page.html_clean)
        _content = ex_content.distance_content(self.page.html_clean, clear=True, article=True,
                                               duplicate=True) if settings.DISTANCE else ex_content.rank_content(
            self.page.html_clean, clear=True)
        _content = html.rebuild(_content, self.page.url)
        _content = html.format_content(_content)
        return _content

    @property
    @store
    def author(self):
        return scan.get_author(self.page.txt)

    @property
    @store
    def time_posted(self):
        return tm.get_timestamp(scan.get_time(self.page.txt))

    @property
    @store
    def come_from(self):
        return scan.get_from(self.page.txt)

    @property
    @store
    def images(self):
        return html.images(self.content)

    @property
    @store
    def rank(self):

        if self.request_all:
            _content = '<p><!--pager--></p>'.join(self.page_contents)
        else:
            _content = self.content

        article = dict(content=_content, title=self.title, keyword=self.keyword, posted_date=self.time_posted)
        stat = score.Score(article)
        return stat.rank