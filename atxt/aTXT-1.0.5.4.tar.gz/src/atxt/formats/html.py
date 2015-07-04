#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jonathan S. Prieto
# @Date:   2015-03-16 02:38:43
# @Last Modified by:   Jonathan Prieto 
# @Last Modified time: 2015-06-30 11:01:24


from _utils import raw_data, save_raw_data, find_encoding
from atxt.log_conf import Logger


log = Logger.log


try:
    import html2text
except:
    log.critical('html2text module not installed')
    log.critical('please: pip install html2text')
    raise Exception('html2text module not installed')
__all__ = ['html']


def html(from_file, to_txt, opts):
    log.debug('html2txt starting')

    h = html2text.HTML2Text()
    h.split_next_td = False
    h.td_count = 0
    h.table_start = False
    h.unicode_snob = 0
    h.escape_snob = 0
    h.links_each_paragraph = 0
    h.body_width = 78
    h.skip_internal_links = True
    h.inline_links = True
    h.protect_links = True
    h.ignore_links = True
    h.ignore_images = True
    h.images_to_alt = True
    h.ignore_emphasis = True
    h.bypass_tables = 1
    h.google_doc = False
    h.ul_item_mark = '*'
    h.emphasis_mark = '_'
    h.strong_mark = '**'
    h.single_line_break = True

    _encoding = find_encoding(from_file.path)
    html = raw_data(from_file.path, _encoding)
    if not html:
        return
    text = h.handle(html)
    return save_raw_data(to_txt.path, text, _encoding)
