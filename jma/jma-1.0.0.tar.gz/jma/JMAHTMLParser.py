# -*- coding: utf-8 -*-

# =================================================================
#
# JMAHTMLParser: modified HTMLParser
#
# =================================================================

from urllib.parse import parse_qs
from html.parser import HTMLParser


class JMAHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)


class ExtractPrefecture(JMAHTMLParser):
    def __init__(self):
        JMAHTMLParser.__init__(self)
        self.prefecture = []
        self.is_in_map = False

    def handle_starttag(self, tag, attrs):
        if (tag == 'map') & (('name', 'point') in attrs):
            self.is_in_map = True

        elif (tag == 'area') & self.is_in_map:
            attrs = dict(attrs)
            attrs_qs = attrs['href'].split('?')[1]
            params = parse_qs(attrs_qs)
            self.prefecture.append((attrs['alt'],
                                    str(params['prec_no'][0])))

    def handle_endtag(self, tag):
        if tag == 'map':
            self.is_in_map = False


class ExtractBlock(ExtractPrefecture):
    def __init__(self):
        JMAHTMLParser.__init__(self)
        self.block = []
        self.is_in_map = False
        self.amedas_or_sokkou = []

    def handle_starttag(self, tag, attrs):
        if (tag == 'map') & (('name', 'point') in attrs):
            self.is_in_map = True

        elif (tag == 'area') & self.is_in_map:
            attrs = dict(attrs)

            try:
                a_or_s = attrs['onmouseover'][21:-2].split(',')[0][1]
            except KeyError:
                a_or_s = ''
            self.amedas_or_sokkou.append(a_or_s)

            attrs_qs = attrs['href'].split('?')[1]
            params = parse_qs(attrs_qs)
            if 'block_no' in params:
                self.block.append((attrs['alt'],
                                   str(params['block_no'][0])))


class ExtractTable(JMAHTMLParser):
    def __init__(self):
        JMAHTMLParser.__init__(self)
        self.table = []
        self.tr = []
        self.is_in_td = False
        self.is_in_tr = False
        self.include_img = False

    def handle_starttag(self, tag, attrs):
        if (tag == 'tr') & (('class', 'mtx') in attrs):
            self.is_in_tr = True
        elif (tag == 'td') & self.is_in_tr:
            self.is_in_td = True
        elif (tag == 'img') & self.is_in_td:
            self.include_img = True

    def handle_endtag(self, tag):
        if (tag == 'td') & self.is_in_td:
            self.is_in_td = False
            self.include_img = False
        elif (tag == 'tr') & self.is_in_tr:
            if self.tr != []:
                self.table.append(self.tr)
                self.tr = []
            self.is_in_tr = False

    def handle_data(self, data):
        if self.is_in_td:
            if data == '':
                if self.include_img:
                    pass
                else:
                    self.tr.append('--')
            else:
                self.tr.append(data)
