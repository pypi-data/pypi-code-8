# -*- coding:utf-8 -*- 
"""
交易数据接口 
Created on 2014/07/31
@author: Jimmy Liu
@group : waditu
@contact: jimmysoa@sina.cn
"""
from __future__ import division

import time
import json
import urllib2
import lxml.html
from lxml import etree
import pandas as pd
import numpy as np
from tushare.stock import cons as ct
from pandas.io.common import urlopen
from pandas.util.testing import _network_error_classes
import re
from StringIO import StringIO
from tushare.util import dateutil as du


def get_hist_data(code=None, start=None, end=None,
                  ktype='D', retry_count=3,
                  pause=0.001):
    """
        获取个股历史交易记录
    Parameters
    ------
      code:string
                  股票代码 e.g. 600848
      start:string
                  开始日期 format：YYYY-MM-DD 为空时取到API所提供的最早日期数据
      end:string
                  结束日期 format：YYYY-MM-DD 为空时取到最近一个交易日数据
      ktype：string
                  数据类型，D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D
      retry_count : int, 默认 3
                 如遇网络等问题重复执行的次数 
      pause : int, 默认 0
                重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
    return
    -------
      DataFrame
          属性:日期 ，开盘价， 最高价， 收盘价， 最低价， 成交量， 价格变动 ，涨跌幅，5日均价，10日均价，20日均价，5日均量，10日均量，20日均量，换手率
    """
    symbol = code_to_symbol(code)
    url = ''
    if ktype.upper() in ct.K_LABELS:
        url = ct.DAY_PRICE_URL%(ct.P_TYPE['http'], ct.DOMAINS['ifeng'],
                                ct.K_TYPE[ktype.upper()], symbol)
    elif ktype in ct.K_MIN_LABELS:
        url = ct.DAY_PRICE_MIN_URL%(ct.P_TYPE['http'], ct.DOMAINS['ifeng'],
                                    symbol, ktype)
    else:
        raise TypeError('ktype input error.')
    
    for _ in range(retry_count):
        time.sleep(pause)
        try:
            with urlopen(url) as resp:
                lines = resp.read()
        except _network_error_classes:
            pass
        else:
            js = json.loads(lines)
            cols = []
            if (code in ct.INDEX_LABELS) & (ktype.upper() in ct.K_LABELS):
                cols = ct.INX_DAY_PRICE_COLUMNS
            else:
                cols = ct.DAY_PRICE_COLUMNS
            df = pd.DataFrame(js['record'], columns=cols)
            if ktype.upper() in ['D','W','M']:
                df = df.applymap(lambda x: x.replace(u',', u''))
            for col in cols[1:]:
                df[col] = df[col].astype(float)
            if start is not None:
                df = df[df.date >= start]
            if end is not None:
                df = df[df.date <= end]
            if (code in ct.INDEX_LABELS) & (ktype in ct.K_MIN_LABELS):
                df = df.drop('turnover', axis=1)
            df = df.set_index('date')
            return df
    raise IOError("%s获取失败，请检查网络和URL:%s" % (code, url))


def _parsing_dayprice_json(pageNum=1):
    """
           处理当日行情分页数据，格式为json
     Parameters
     ------
        pageNum:页码
     return
     -------
        DataFrame 当日所有股票交易数据(DataFrame)
    """
    print 'getting page %s ...'%pageNum
    url = ct.SINA_DAY_PRICE_URL%(ct.P_TYPE['http'], ct.DOMAINS['vsf'],
                                 ct.PAGES['jv'], pageNum)
    request = urllib2.Request(url)
    text = urllib2.urlopen(request, timeout=10).read()
    if text == 'null':
        return None
    reg = re.compile(r'\,(.*?)\:') 
    #修改成read_json能读入的json格式
    text = reg.sub(r',"\1":', text) 
    text = text.replace('"{symbol', '{"symbol')
    text = text.replace('{symbol', '{"symbol"')
    jstr = json.dumps(text, encoding='GBK')
    js = json.loads(jstr)
    df = pd.DataFrame(pd.read_json(js, dtype={'code':object}),
                      columns=ct.DAY_TRADING_COLUMNS)
    #删除原始数据的symbol属性
    df = df.drop('symbol', axis=1)
    #删除停牌的股票
    df = df.ix[df.volume > 0]
    return df


def get_tick_data(code=None, date=None, retry_count=3, pause=0.001):
    """
        获取分笔数据
    Parameters
    ------
        code:string
                  股票代码 e.g. 600848
        date:string
                  日期 format：YYYY-MM-DD
        retry_count : int, 默认 3
                  如遇网络等问题重复执行的次数
        pause : int, 默认 0
                 重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
     return
     -------
        DataFrame 当日所有股票交易数据(DataFrame)
              属性:成交时间、成交价格、价格变动，成交手、成交金额(元)，买卖类型
    """
    if code is None or len(code)!=6 or date is None:
        return None
    symbol = code_to_symbol(code)
    url = ct.TICK_PRICE_URL % (ct.P_TYPE['http'], ct.DOMAINS['sf'], ct.PAGES['dl'],
                                date, symbol)
    for _ in range(retry_count):
        time.sleep(pause)
        try:
            re = urllib2.Request(url)
            lines = urllib2.urlopen(re, timeout=10).read()
            lines = lines.decode('GBK')      
        except _network_error_classes:
            pass
        else:
            df = pd.read_table(StringIO(lines), names=ct.TICK_COLUMNS,
                               skiprows=[0]) 
            return df
    raise IOError("%s获取失败，请检查网络和URL:%s" % (code, url))
    
    
def get_today_all():
    """
        一次性获取最近一个日交易日所有股票的交易数据
    return
    -------
      DataFrame
           属性：代码，名称，涨跌幅，现价，开盘价，最高价，最低价，最日收盘价，成交量，换手率
    """
    df = _parsing_dayprice_json(1)
    if df is not None:
        for i in range(2,ct.PAGE_NUM[0]):
            newdf = _parsing_dayprice_json(i)
            df = df.append(newdf, ignore_index=True)
    return df


def get_realtime_quotes(symbols=None):
    """
        获取实时交易数据 getting real time quotes data
       用于跟踪交易情况（本次执行的结果-上一次执行的数据）
    Parameters
    ------
        symbols : string, array-like object (list, tuple, Series).
        
    return
    -------
        DataFrame 实时交易数据
              属性:0：name，股票名字
            1：open，今日开盘价
            2：pre_close，昨日收盘价
            3：price，当前价格
            4：high，今日最高价
            5：low，今日最低价
            6：bid，竞买价，即“买一”报价
            7：ask，竞卖价，即“卖一”报价
            8：volumn，成交量 maybe you need do volumn/100
            9：amount，成交金额（元 CNY）
            10：b1_v，委买一（笔数 bid volume）
            11：b1_p，委买一（价格 bid price）
            12：b2_v，“买二”
            13：b2_p，“买二”
            14：b3_v，“买三”
            15：b3_p，“买三”
            16：b4_v，“买四”
            17：b4_p，“买四”
            18：b5_v，“买五”
            19：b5_p，“买五”
            20：a1_v，委卖一（笔数 ask volume）
            21：a1_p，委卖一（价格 ask price）
            ...
            30：date，日期；
            31：time，时间；
    """
    symbols_list = ''
    if type(symbols) is list or type(symbols) is set or type(symbols) is tuple or type(symbols) is pd.Series:
        for code in symbols:
            symbols_list += code_to_symbol(code) + ','
    else:
        symbols_list = code_to_symbol(symbols)
        
    symbols_list = symbols_list[:-1] if len(symbols_list) > 8 else symbols_list 
    request = urllib2.Request(ct.LIVE_DATA_URL%(ct.P_TYPE['http'], ct.DOMAINS['sinahq'],
                                                random(), symbols_list))
    text = urllib2.urlopen(request,timeout=10).read()
    text = text.decode('GBK')
    reg = re.compile(r'\="(.*?)\";')
    data = reg.findall(text)
    regSym = re.compile(r'(?:sh|sz)(.*?)\=')
    syms = regSym.findall(text)
    data_list = []
    for row in data:
        if len(row)>1:
            data_list.append([astr for astr in row.split(',')])
    df = pd.DataFrame(data_list, columns=ct.LIVE_DATA_COLS)
    df = df.drop('s', axis=1)
    df['code'] = syms
    ls = [cls for cls in df.columns if '_v' in cls]
    for txt in ls:
        df[txt] = df[txt].map(lambda x : x[:-2])
    return df


def get_h_data(code, start=None, end=None, autype='qfq',
               retry_count=3, pause=0.001):
    '''
    获取历史复权数据
    Parameters
    ------
      code:string
                  股票代码 e.g. 600848
      start:string
                  开始日期 format：YYYY-MM-DD 为空时取当前日期
      end:string
                  结束日期 format：YYYY-MM-DD 为空时取去年今日
      autype:string
                  复权类型，qfq-前复权 hfq-后复权 None-不复权，默认为qfq
      retry_count : int, 默认 3
                 如遇网络等问题重复执行的次数 
      pause : int, 默认 0
                重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
    return
    -------
      DataFrame
          date 交易日期 (index)
          open 开盘价
          high  最高价
          close 收盘价
          low 最低价
          volumn 成交量
          amount 成交金额
    '''
    
    start = du.today_last_year() if start is None else start
    end = du.today() if end is None else end
    qs = du.get_quarts(start, end)
    qt = qs[0]
    print ct.FQ_PRINTING%(qt[0], qt[1])
    data = _parse_fq_data(ct.HIST_FQ_URL%(ct.P_TYPE['http'], ct.DOMAINS['vsf'],
                              code, qt[0], qt[1]), retry_count, pause)
    if len(qs)>1:
        for d in range(1, len(qs)):
            qt = qs[d]
            print ct.FQ_PRINTING%(qt[0], qt[1])
            url = ct.HIST_FQ_URL%(ct.P_TYPE['http'], ct.DOMAINS['vsf'],
                                  code, qt[0], qt[1])
            df = _parse_fq_data(url, retry_count, pause)
            data = data.append(df, ignore_index=True)
    data = data.drop_duplicates('date')
    if start is not None:
        data = data[data.date>=start]
    if end is not None:
        data = data[data.date<=end]
    if autype == 'hfq':
        data = data.drop('factor', axis=1)
        for label in ['open', 'high', 'close', 'low']:
            data[label] = data[label].map(ct.FORMAT)
        data = data.set_index('date')
        data = data.sort_index(ascending=False)
        return data
    else:
        for label in ['open', 'high', 'close', 'low']:
            data[label] = data[label] / data['factor']
        data = data.drop('factor', axis=1)
        if autype == 'qfq':
            df = _parase_fq_factor(code, start, end)
            df = df.drop_duplicates('date')
            df = df[df.date>=start]
            df = df[df.date<=end]
            df = pd.merge(data, df)
            df = df.sort('date', ascending=False)
            frow = df.head(1)
            rate = float(frow['close']) / float(frow['factor'])
            df['close_temp'] = df['close']
            df['close'] = rate * df['factor']
            for label in ['open', 'high', 'low']:
                df[label] = df[label] * (df['close'] / df['close_temp'])
                df[label] = df[label].map(ct.FORMAT)
            df = df.drop(['factor', 'close_temp'], axis=1)
            df['close'] = df['close'].map(ct.FORMAT)
            df = df.set_index('date')
            df = df.sort_index(ascending=False)
            return df
        else:
            for label in ['open', 'high', 'close', 'low']:
                data[label] = data[label].map(ct.FORMAT)
            data = data.set_index('date')
            data = data.sort_index(ascending=False)
            return data


def _parase_fq_factor(code, start, end):
    from tushare.util import demjson
    symbol = code_to_symbol(code)
    url = ct.HIST_FQ_FACTOR_URL%(ct.P_TYPE['http'], ct.DOMAINS['vsf'], symbol)
    request = urllib2.Request(url)
    text = urllib2.urlopen(request, timeout=10).read()
    text = text[1:len(text)-1]
    text = demjson.decode(text)
    df = pd.DataFrame({'date':text['data'].keys(), 'factor':text['data'].values()})
    df['date'] = df['date'].map(lambda x:x[1:].replace('_', '-'))
    if df['date'].dtypes == np.object:
        df['date'] = df['date'].astype(np.datetime64)
    df = df.drop_duplicates('date')
    df['factor'] = df['factor'].astype(float)
    return df


def _parse_fq_data(url, retry_count, pause):
    for _ in range(retry_count):
        time.sleep(pause)
        try:
            html = lxml.html.parse(url)  
            res = html.xpath('//table[@id=\"FundHoldSharesTable\"]')
            sarr = [etree.tostring(node) for node in res]
            sarr = ''.join(sarr)
            df = pd.read_html(sarr, skiprows=[0, 1])[0]
            df.columns = ct.HIST_FQ_COLS
        except _network_error_classes:
            pass
        else:
            if df['date'].dtypes == np.object:
                df['date'] = df['date'].astype(np.datetime64)
            df = df.drop_duplicates('date')
            return df
    raise IOError("获取失败，请检查网络和URL:%s" % url)


def random(n=13):
    from random import randint
    start = 10**(n-1)
    end = (10**n)-1
    return str(randint(start, end))


def code_to_symbol(code):
    """
        生成symbol代码标志
    """
    if code in ct.INDEX_LABELS:
        return ct.INDEX_LIST[code]
    else:
        if len(code) != 6 :
            return ''
        else:
            return 'sh%s'%code if code[:1] == '6' else 'sz%s'%code
