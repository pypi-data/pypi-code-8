# -*- coding:utf-8 -*- 
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request
    

def fortest():
#     mycookie = HTTPCookieProcessor(cookielib.CookieJar())
#     opener = poster.streaminghttp.register_openers()
    url = 'http://query.sse.com.cn/marketdata/tradedata/queryMargin.do?jsonCallBack=jsonpCallback%s&isPagination=true&tabType=&pageHelp.pageSize=100&_=%s'
    url = url%(_random(5), _random(13))
    print(url)
    request = Request(url)
    request.add_header("Accept-Language", "en-US,en;q=0.5")
    request.add_header("Connection", "keep-alive")
#     request.add_header("X-Requested-With", "XMLHttpRequest")
    request.add_header('Referer', 'http://www.sse.com.cn/market/dealingdata/overview/margin/')
#     cookie_str = "_gscu_1808689395=27850607moztu036"
#     request.add_header("Cookie", cookie_str)
#     data_str = openner.open(request).read()
    lines = urlopen(request, timeout = 10).read()
    print(lines)

def _random(n=13):
    from random import randint
    start = 10**(n-1)
    end = (10**n)-1
    return str(randint(start, end))

if __name__ == '__main__':
    fortest()