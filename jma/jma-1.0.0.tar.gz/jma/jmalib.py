#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =================================================================
#
# jmalib.py: get weather statistics from JMA
#
# =================================================================

import urllib.request
import urllib.parse
from .JMAHTMLParser import ExtractTable, ExtractPrefecture, ExtractBlock


class JMA:
    def __init__(self):
        self.view_path = "http://www.data.jma.go.jp/obd/stats/etrn/view/"
        self.select_path = "http://www.data.jma.go.jp/obd/stats/etrn/select/"

    def extract_table(self, date, location_params, amedas_or_sokkou,
                      hourly_or_ten):
        if amedas_or_sokkou == 'a':
            view_param = ''
        else:
            view_param = ''
        table_params_dict = {
            'year': date.year,
            'month': date.month,
            'day': date.day,
            'elm': 'hourly',
            'view': view_param
            }
        table_params_dict.update(location_params)
        params = urllib.parse.urlencode(table_params_dict)

        if hourly_or_ten == 'hourly':
            table_url = self.view_path + 'hourly_' + amedas_or_sokkou\
                + '1.php' + '?' + params
        elif hourly_or_ten == 'ten':
            table_url = self.view_path + '10min_' + amedas_or_sokkou\
                + '1.php' + '?' + params
        f = urllib.request.urlopen(table_url)

        parser = ExtractTable()
        parser.feed(f.read().decode('utf-8'))
        parser.close()
        return parser.table

    def extract_prefecture(self):
        f = urllib.request.urlopen(self.select_path + 'prefecture00.php')

        parser = ExtractPrefecture()
        parser.feed(f.read().decode('utf-8'))
        parser.close()
        return parser.prefecture

    def extract_block(self, pref_params_dict):
        params = urllib.parse.urlencode(pref_params_dict)
        f = urllib.request.urlopen(self.select_path + 'prefecture.php' +
                                   '?' + params)

        parser = ExtractBlock()
        parser.feed(f.read().decode('utf-8'))
        parser.close()
        return (parser.block, parser.amedas_or_sokkou)
