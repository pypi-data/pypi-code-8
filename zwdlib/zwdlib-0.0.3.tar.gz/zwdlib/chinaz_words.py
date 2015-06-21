# encoding: utf-8
'''
Created on 2015年3月30日

@author: Lenovo
'''
import urllib
import urllib2

from pyquery.pyquery import PyQuery
from tool_html import remove_garbages
from tool_net import fetch


def parse_keywords(html):
    d = PyQuery(html)
    records = []
    for x in d('tr.seo_item'):
        tds = [i.text() for i in PyQuery(x).items('td')]
        if tds and len(tds) >= 3: 
            records.append({'name':tds[1],
                             
                            'index':int(tds[2])
                            })
    return records

def search_keywords(kw):
    url = "http://s.tool.chinaz.com/baidu/words.aspx"
    cookie = "Hm_lvt_aecc9715b0f5d5f7f34fba48a3c511d6=1422794482; Hm_lpvt_aecc9715b0f5d5f7f34fba48a3c511d6=1422794482; PHPSESSID=n9049t1uj8281sq51fg0khpmh5"
    data = fetch(url, paras=urllib.urlencode({"kw": kw.encode('utf8')}), 
                 cookie = cookie,
                 referer= "http://s.tool.chinaz.com/baidu/words.aspx",
                 user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36")

    return parse_keywords(data)        
    
    
if __name__ == '__main__':
    html = open('debug.html','rb').read().decode('utf8')
    parse_keywords(html)

    for x in search_keywords(u'起名'):
        print x