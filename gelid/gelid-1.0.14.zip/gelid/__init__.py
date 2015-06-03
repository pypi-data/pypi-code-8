# -*- coding: UTF-8 -*-
# lvjiyong on 2015/4/19.
from gelid.extractors import html, score, tm, scan, regex, content, http, page, title, xpath
from gelid.items import article
from gelid.extractors.log import logger

html = html
score = score
tm = tm
scan = scan
regex = regex
content = content
http = http
page = page
title = title
xpath = xpath
Article = article.Article


def config(request_timeout):
    http.request_timeout = request_timeout