'''
Created on 2014-7-18

@author: Winston Zhong
'''

from agent_lite import pick_one_agent
import StringIO
import cookielib
import gzip
import re
import urllib2
import urlparse

ptn_ip = re.compile("\d+\.\d+\.\d+\.\d+")

def search_first_ip(html):
    '''
    Return first ip address found by regx
    >>> search_first_ip('dalfj 12.12.12.12')
    '12.12.12.12'
    >>> search_first_ip('dalfj 12.12.12')
    >>> search_first_ip(None)    
    '''
    if html:
        m = ptn_ip.search(html)
        if m:
            return m.group(0)

def get_public_ip():
    sites = (
             "http://www.ip138.com/ips138.asp",
            "http://ip.cn/",
            "http://www.whereismyip.com/"
             )
    for url in sites:
        try:
            content = urllib2.urlopen(url, timeout=10).read()
            return search_first_ip(content)
        except:
            pass 
        
def get_host(url):
    return urlparse.urlsplit(url).hostname or ""


class DummyOpener(object):
    def __init__(self):
        self.open = urllib2.urlopen


def get_opener(ip, port, proxy):
    if proxy:
        ip,port = proxy.get('ip_port').split(':')
    
    if ip and port and ip != 'localhost':
        cj = cookielib.LWPCookieJar()
        cookie_support = urllib2.HTTPCookieProcessor(cj)
        
        proxy_info = {  
                'host' : ip,
                'port' : int(port)
        }
        proxy_support = urllib2 . ProxyHandler ( { 'http' : \
                                                  
                'http://%(host)s:%(port)d' % proxy_info } ) 
        
        return urllib2.build_opener(cookie_support, proxy_support)
    else:
        return DummyOpener()
    

def fetch(url, ip=None, port=None, timeout=30, referer='', cookie='', paras=None, header={}, proxy=None, user_agent = pick_one_agent()):
    opener = get_opener(ip, port, proxy)
    headers = { 
               'Host': get_host(url),
               'Accept': '*/*',
               'Accept-Language': 'zh-cn,en-us;q=0.5',
               'Accept-Encoding': 'gzip, deflate',
               'User-Agent' : user_agent,
               'Accept-Charset': 'GB2312,utf-8;q=0.7,*;q=0.7',
               'Referer':referer, 
               'Cookie' : cookie,
               }
    
    if header:
        headers.update(header)
    
    req = urllib2.Request(url, headers=headers)

    response = opener.open(req,timeout=timeout, data=paras)


    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO.StringIO( response.read())
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()    
    else:
        data = response.read()
    response.close()
    
    return data

def fetch_ip138(proxy=None):
    return fetch("http://20140507.ip138.com/ic.asp", proxy=proxy)

# def open_retry(page, data=None, referer=None,retry = 3,cookies='',sleep_time=3,ip=None,port=None,timeout=30):
# #     time.sleep(sleep_time)
# #     print page
#     if not referer:
#         referer = page
#     fails = 0
#     while True:
#         try:
#             if fails >= retry:
#                 break
#              
#             headers={'referer':referer,
# #                      'host': 'jobs.zhaopin.com',
#                     'user-agent':pick_one_agent(),
# #                     'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
# #                     'Accept-Encoding':'gzip,deflate,sdch',
# #                     'Accept-Language':'zh-CN,zh;q=0.8',
# #                     'Cache-Control':'max-age=0',
# #                     'Connection':'keep-alive',
# #                     'Cookie':'urlfrom2=121122523; adfcid2=bd_kw_zdty_sc_cd_0_000008; adfbid2=0; dywez=95841923.1385966970.3.3.dywecsr=google.com.hk|dyweccn=(referral)|dywecmd=referral|dywectr=undefined|dywecct=/; firstchannelurl=http%3A//my.zhaopin.com/; lastchannelurl=http%3A//my.zhaopin.com/; JSSearchModel=0; LastCity%5Fid=530; LastCity=%e5%8c%97%e4%ba%ac; dywea=95841923.2399871165886883000.1381800773.1383150212.1385966970.3; dywec=95841923; dyweb=95841923.32.9.1385967498945; __utma=269921210.862386675.1381800773.1383150208.1385966969.3; __utmb=269921210.32.9.1385967498945; __utmc=269921210; __utmz=269921210.1385966969.3.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)'
#                     'Cookie':cookies
# #                    'Cookie': 'verifysession=h00a5fbf958e27d31cc2828e201bd70f49cf0eb487aa72a5636aabb164fb850e5a7a2810782bf0eb4084095cfe9e6172549'
# #                     'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
# #                     "Cookie":'cookie2=affc7ecae5dde88dff6fbd43eb4f7c10; t=786bbbfc1e14bb5dc1672470099f1c82; v=0; mt=ci=0_0; cna=TqUsCnY2dEECAavYd4bj4cX1; tip_showed=true; _sortbar_stick_=1; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0'
#                     }
#             
#             page=urllib2.Request(page,headers=headers) 
# #             print [ip,port]
#             if ip and port:
#                 proxy = {'http':'%s:%s'%(ip,port)}
#             else:
#                 proxy = {}
# #             print proxy
#             proxy_support = urllib2.ProxyHandler(proxy)
#             opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
#             urllib2.install_opener(opener)
#             return urllib2.urlopen(page, data,timeout=timeout).read()
#         except:
# #             buf = StringIO.StringIO()
# #             traceback.print_exc(file=buf)
# #             print buf.getvalue()
#             
#             fails += 1
# #             print 'retry'
#             time.sleep(sleep_time)
# #             print "fails:%d" %fails
#         else:
# #            self.timeout = True
#             break



if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True, report=True)

