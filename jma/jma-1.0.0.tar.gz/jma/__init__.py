#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import date, timedelta
import sys
import csv
import codecs
from .jmalib import JMA

sys_encoding = sys.stdout.encoding
# sys_encoding = sys.getfilesystemencoding()


def ask_date():
    print("Beginning date of data you want.")
    d_start_year = int(input("    year? "))
    d_start_month = int(input("    month? "))
    d_start_date = int(input("    date? "))
    d_start = date(d_start_year, d_start_month, d_start_date)

    print("Final date of data you want.")
    d_end_year = int(input("    year? "))
    d_end_month = int(input("    month? "))
    d_end_date = int(input("    date? "))
    d_end = date(d_end_year, d_end_month, d_end_date)

    return (d_start, d_end)


def ask_location(jma):
    print("Choose location:")
    pref_list = jma.extract_prefecture()
    for i in range(len(pref_list)):
        p = pref_list[i]
        # print("    %s: %s" % (i, p[0].decode('sjis').encode(sys_encoding)))
        # print("    %s: %s" % (i, p[0].decode('sjis')))
        # print("    %s: %s" % (i, p[0].decode('utf-8')))
        print("    {0}: {1}".format(i, p[0]))

    pref_num = int(input("  Choose prefecture (number): "))
    pref_params = {'prec_ch': pref_list[pref_num][0],
                   'prec_no': pref_list[pref_num][1]}

    extracted_blocks = jma.extract_block(pref_params)
    block_list = extracted_blocks[0]
    amedas_or_sokkou = extracted_blocks[1]
    for i in range(len(block_list)):
        if i % 2 == 0:
            b = block_list[i]
            # print("    %s: %s" %
            #       (i, b[0].decode('sjis').encode(sys_encoding)))
            # print("    %s: %s" % (i, b[0].decode('sjis')))
            # print("    %s: %s" % (i, b[0].decode('utf-8')))
            print("    {0}: {1}".format(int(i/2), b[0]))

    block_num = 2 * int(input("  Choose block (number): "))
    block_params = {'block_ch': block_list[block_num][0],
                    'block_no': block_list[block_num][1]}

    pref_params.update(block_params)
    return (pref_params, amedas_or_sokkou[block_num])


def ask_time_interval(amedas_or_sokkou):
    hourly_s_table_header = ['年月日', '時間', '気圧 (hPa; 現地)',
                             '気圧 (hPa; 海面)', '降水量 (mm)',
                             '気温 (oC)', '露点温度 (oC)', '蒸気圧 (hPa)',
                             '湿度 (%)', '風速 (m/s)', '風向',
                             '日照時間 (h)', '全天日射 (MJ/m3)',
                             '降雪 (cm)', '積雪 (cm)', '天気', '雲量',
                             '視程 (km)']
    hourly_a_table_header = ['年月日', '時間', '降水量 (mm)', '気温 (oC)',
                             '風速 (m/s)', '風向', '日照時間 (h)',
                             '降雪 (cm)', '積雪 (cm)']
    ten_min_s_table_header = ['年月日', '時間', '気圧 (hPa; 現地)',
                              '気圧 (hPa; 海面)', '降水量 (mm)', '気温 (oC)',
                              '相対湿度 (%)', '平均風速 (m/s)', '平均風向',
                              '最大瞬間風速 (m/s)', '最大瞬間風向',
                              '日照時間 (h)']
    ten_min_a_table_header = ['年月日', '時間', '降水量 (mm)', '気温 (oC)',
                              '平均風速 (m/s)', '平均風向',
                              '最大瞬間風速 (m/s)', '最大瞬間風向',
                              '日照時間 (h)']

    time_interval = {'1': 'hourly',
                     '2': 'ten'}

    print("Choose time interval")
    t = int(input("  1: Hourly    2: 10 min.: "))

    if amedas_or_sokkou == 'a':
        if t == 1:
            return (time_interval[str(t)], hourly_a_table_header)
        elif t == 2:
            return (time_interval[str(t)], ten_min_a_table_header)
    elif amedas_or_sokkou == 's':
        if t == 1:
            return (time_interval[str(t)], hourly_s_table_header)
        elif t == 2:
            return (time_interval[str(t)], ten_min_s_table_header)


def main():
    jma = JMA()

    asked_date = ask_date()
    d_start = asked_date[0]
    d_end = asked_date[1]
    if d_start > d_end:
        d_start, d_end = d_end, d_start
    d = d_start

    asked_location = ask_location(jma)
    location_params = asked_location[0]
    amedas_or_sokkou = asked_location[1]

    asked_ti = ask_time_interval(amedas_or_sokkou)
    time_interval = asked_ti[0]
    table_header = asked_ti[1]

    stat_csv_file_name = input("saving file name? ")
    with codecs.open(stat_csv_file_name, 'w', 'shift_jis') as stat_csv:
        csv_writer = csv.writer(stat_csv, dialect=csv.excel)
        csv_writer.writerow([i for i in table_header])

        while d <= d_end:
            print("  Retrieving data on {0} ...".format(d.isoformat()))
            jma_table = jma.extract_table(d, location_params,
                                          amedas_or_sokkou,
                                          time_interval)
            for row in jma_table:
                row_with_date = [d.isoformat()] + [x for x in row]
                csv_writer.writerow(row_with_date)
            d += timedelta(days=1)

    print("Done.")
