# -*- coding: utf8 -*-
from agent import pick_one_agent
from decimal import Decimal
import StringIO
import chardet
import datetime
import hashlib
import json
import os
import re
import six
import time
import traceback
import urllib2
import urlparse
import uuid

# ptn_empty_space = re.compile('\s*')
ptn_empty_space = re.compile('\s+', re.MULTILINE)

ptn_link = re.compile("<a.+?href=.+?>(.+?)</a>",re.DOTALL)
ptn_tag = re.compile("<.+?>", re.DOTALL)

def _force_unicode(txt):
    raise ValueError, "this function is corrupted"
#     django

class DjangoUnicodeDecodeError(UnicodeDecodeError):
    def __init__(self, obj, *args):
        self.obj = obj
        UnicodeDecodeError.__init__(self, *args)

    def __str__(self):
        original = UnicodeDecodeError.__str__(self)
        return '%s. You passed in %r (%s)' % (original, self.obj,
                type(self.obj))
        
def is_protected_type(obj):
    """Determine if the object instance is of a protected type.

    Objects of protected types are preserved as-is when passed to
    force_text(strings_only=True).
    """
    return isinstance(obj, six.integer_types + (type(None), float, Decimal,
        datetime.datetime, datetime.date, datetime.time))
    
def force_unicode(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Similar to smart_text, except that lazy instances are resolved to
    strings, rather than kept as lazy objects.

    If strings_only is True, don't convert (some) non-string-like objects.
    
    >>> txt='\xe5\xa5\xbd'
    >>> force_unicode(txt,encoding='utf-8')
    u'\u597d'
    
    >>> txt='\xba\xc3'
    >>> force_unicode(txt,encoding='cp936')
    u'\u597d'
    
    >>> txt=u'\u597d'
    >>> force_unicode(txt,encoding='cp936')
    u'\u597d'
    """
    # Handle the common case first, saves 30-40% when s is an instance of
    # six.text_type. This function gets called often in that setting.
    if isinstance(s, six.text_type):
        return s
    if strings_only and is_protected_type(s):
        return s
    try:
        if not isinstance(s, six.string_types):
            if hasattr(s, '__unicode__'):
                s = s.__unicode__()
            else:
                if six.PY3:
                    if isinstance(s, bytes):
                        s = six.text_type(s, encoding, errors)
                    else:
                        s = six.text_type(s)
                else:
                    s = six.text_type(bytes(s), encoding, errors)
        else:
            # Note: We use .decode() here, instead of six.text_type(s, encoding,
            # errors), so that if s is a SafeBytes, it ends up being a
            # SafeText at the end.
            s = s.decode(encoding, errors)
    except UnicodeDecodeError as e:
        if not isinstance(s, Exception):
            raise DjangoUnicodeDecodeError(s, *e.args)
        else:
            # If we get to here, the caller has passed in an Exception
            # subclass populated with non-ASCII bytestring data without a
            # working unicode method. Try to handle this without raising a
            # further exception by individually forcing the exception args
            # to unicode.
            s = ' '.join([force_unicode(arg, encoding, strings_only,
                    errors) for arg in s])
    return s


def is_chinese(uchar,charset=None):
    
    '''
    >>> is_chinese('你',charset='utf8')
    True
    >>> is_chinese('a')
    False
    >>> is_chinese('.')
    False
    '''
    if charset:
        uchar = uchar.decode(charset)
#     print [uchar]
    if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
        return True
    else:
        return False    

def has_chinese(uchars):
    for u in uchars:
        if is_chinese(u):
            return True
    return False


def is_string(tag):
    '''
    >>> is_string('abc')
    True
    >>> is_string(12)
    False
    >>> is_string(None)
    False
    >>> is_string(u'你好')
    True
    >>> is_string(datetime.datetime.now())
    False
    '''
    return isinstance(tag, str) or isinstance(tag, unicode) 

def remove_space(text):
    '''
    >>> remove_space('ab c')
    'abc'
    '''
    return ptn_empty_space.sub('', text)

def replace_spaces(text):
    '''
    >>> replace_spaces('ab   \\r\\nc')
    'ab c'
    '''
    return ptn_empty_space.sub(' ', text)


def convert2encoding(fpath, from_encoding, toencoding):
    content = open(fpath,'rb').read().decode(from_encoding).encode(toencoding,'ignore')
    fp = open(fpath,'wb')
    fp.write(content)
    fp.close()
    
def get_filename_by_path(path):
    path = path.replace('\\','/')
    filename = path.split('/')[-1]
#     print filename
    return filename

def remove_links(txt):
    '''
    >>> remove_links("<a href='www.baidu.com'>a</a>")
    'a'
    '''
    return ptn_link.sub(r'\1', txt)


# json处理datetime
class ComplexEncode(json.JSONEncoder):
    def default(self, obj):
#         print type(datetime.datetime)
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

def get_china_now():
    return datetime.datetime.utcnow() + datetime.timedelta(hours=8)

def get_md5(txt):
    '''
    >>> get_md5('a')
    '0cc175b9c0f1b6a831c399e269772661'
    '''
#     print [txt]
    txt = str(txt)
    m = hashlib.md5(txt).hexdigest()
#     m.update(txt)
#     res = m.hexdigest()
    return m

def force_unicode2(txt):
    if isinstance(txt,unicode) or not txt:
        return txt or ''
    ecd = chardet.detect(txt)['encoding']
    if ecd == 'utf-8' or ecd == 'utf8':
        return txt.decode(ecd)
    else:
        return txt.decode('cp936')

def remove_tags(txt):
#     print 'remove_tags',[txt]
    '''
    >>> remove_tags('<html>abc</html>')
    'abc'
    >>> remove_tags('')
    ''
    >>> remove_tags(1.2)
    1.2
    '''
    if txt and (isinstance(txt,str) or isinstance(txt,unicode)):
        return ptn_tag.sub('', txt)
    else:
        return txt

def force_utf8(txt):
    try:
        return txt.encode('utf8')
    except:
        return txt

def is_timeout(dt_last,dt_current=get_china_now(),timeout=3600):
    '''
    >>> dt = datetime.datetime(1999,12,1,1,1)
    >>> is_timeout(dt)
    True
    >>> dt_current = datetime.datetime(1999,12,1,1,2)
    >>> is_timeout(dt,dt_current)
    False
    >>> timeout = 10  
    >>> is_timeout(dt,dt_current,timeout)
    True
    '''
    if dt_current - dt_last > datetime.timedelta(seconds=timeout):
        return True
    return False

def get_brief_content(txt,max_len=20):
    '''
    >>> txt = 'abcdfasdfasdfasdfaldslfja;lsdkjf;lasjdflk'
    >>> get_brief_content(txt)
    'abcdfasdfasdfasdfald...'
    >>> txt = 'abcd'
    >>> get_brief_content(txt)
    'abcd'
    >>> get_brief_content(None)
    >>> get_brief_content(['a'])
    ['a']
    '''
    if txt and (isinstance(txt,str) or isinstance(txt,unicode)) and len(txt) > max_len:
        txt = txt[:max_len] + '...'
    return txt

def force_int(num,default=0):
    '''
    >>> force_int('1')
    1
    >>> force_int('a')
    0
    >>> force_int(None)
    0
    '''
    
    try:
        num = int(num)
    except:
        num =default
    return num

def get_mac_address():
    node = uuid.getnode()
    mac = uuid.UUID(int = node).hex[-12:]
    return mac

def get_file_format(path):
    if "." in path:
        path = path.split(".")
        return path[-1].lower()
    else:
        return None           
        
def get_all_path(dir,topdown=True, get_dirs=True, get_path=True, format_keep=[]):
    """
        args:
        
        format_keep - specific file format to keep; such as: 'txt'
        
        return: 
        (dir_list, path_list)
        
        dir_list - all dirs below the given dir
        
        path_list - all paths below the given dir
    """
    dir_list = []
    path_list = []
    for root, dirs, files in os.walk(dir, topdown):
        if get_path == True:
            for name in files:
                current_path = os.path.join(root,name)
                if format_keep:
                    for format in format_keep:
                        format = format.lower()
                        file_format = get_file_format(current_path)
                        if file_format.lower() == format:
#                            print current_path
                            path_list.append(current_path)
                else:
#                    print current_path
                    path_list.append(current_path)
        if get_dirs == True:                     
            for name in dirs:
                current_dir = os.path.join(root,name)
#                print current_dir
                dir_list.append(current_dir)
    return dir_list,path_list




def is_img(url):
    '''
    >>> url = 'http://www.baidu.com/1.gif'
    >>> is_img(url)
    True
    >>> url = 'http://www.baidu.com/1.jpg?a=1&b=2'
    >>> is_img(url)
    True
    >>> url = 'http://www.baidu.com/1.jpg&a=1&b=2'
    >>> is_img(url)
    True
    >>> url = 'http://www.baidu.com/1&a=1&b=2'
    >>> is_img(url)
    False
    '''  
    
    path = urlparse.urlparse(url).path
    path = path.split('&')[0]
    format_list = ['.gif','.jpg','.jpeg','.png','.bmp']
    for img_format in format_list:
        if path.endswith(img_format):
            return True
    return False

def create_dir(dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

def get_dir_by_fpath(path):
    '''
    >>> path = 'c:/aa/bb.txt'
    >>> get_dir_by_fpath(path)
    'c:/aa'
    >>> path = '/aa/bb.txt'
    >>> get_dir_by_fpath(path)
    '/aa'
    '''

    path = path.replace('\\','/')
#     print path
    dest_dir = '/'.join(path.split('/')[:-1])
    return dest_dir

def remove_file_garbage(txt):
    if txt and txt.startswith(u'\ufffd'):
        txt = txt.replace(u'\ufffd','')
    return txt

def open_retry(page, data=None, referer=None,retry = 3,cookies='',sleep_time=3,ip=None,port=None,timeout=30):
    if not referer:
        referer = page
    fails = 0
    while True:
        try:
            if fails >= retry:
                break
             
            headers={'referer':referer,
#                      'host': 'jobs.zhaopin.com',
                    'user-agent':pick_one_agent(),
#                     'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#                     'Accept-Encoding':'gzip,deflate,sdch',
#                     'Accept-Language':'zh-CN,zh;q=0.8',
#                     'Cache-Control':'max-age=0',
#                     'Connection':'keep-alive',
#                     'Cookie':'urlfrom2=121122523; adfcid2=bd_kw_zdty_sc_cd_0_000008; adfbid2=0; dywez=95841923.1385966970.3.3.dywecsr=google.com.hk|dyweccn=(referral)|dywecmd=referral|dywectr=undefined|dywecct=/; firstchannelurl=http%3A//my.zhaopin.com/; lastchannelurl=http%3A//my.zhaopin.com/; JSSearchModel=0; LastCity%5Fid=530; LastCity=%e5%8c%97%e4%ba%ac; dywea=95841923.2399871165886883000.1381800773.1383150212.1385966970.3; dywec=95841923; dyweb=95841923.32.9.1385967498945; __utma=269921210.862386675.1381800773.1383150208.1385966969.3; __utmb=269921210.32.9.1385967498945; __utmc=269921210; __utmz=269921210.1385966969.3.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)'
                    'Cookie':cookies
#                    'Cookie': 'verifysession=h00a5fbf958e27d31cc2828e201bd70f49cf0eb487aa72a5636aabb164fb850e5a7a2810782bf0eb4084095cfe9e6172549'
#                     'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
#                     "Cookie":'cookie2=affc7ecae5dde88dff6fbd43eb4f7c10; t=786bbbfc1e14bb5dc1672470099f1c82; v=0; mt=ci=0_0; cna=TqUsCnY2dEECAavYd4bj4cX1; tip_showed=true; _sortbar_stick_=1; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0'
                    }
            
            page=urllib2.Request(page,headers=headers) 
#             print [ip,port]
            if ip and port:
                proxy = {'http':'%s:%s'%(ip,port)}
            else:
                proxy = {}
#             print proxy
            proxy_support = urllib2.ProxyHandler(proxy)
            opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
            urllib2.install_opener(opener)
            return urllib2.urlopen(page,data=data,timeout=timeout).read()
        except:
#             buf = StringIO.StringIO()
#             traceback.print_exc(file=buf)
#             print buf.getvalue()
            
            fails += 1
#             print 'retry'
            time.sleep(sleep_time)
#             print "fails:%d" %fails
        else:
#            self.timeout = True
            break


def open_retry_simple(url,data=None,retry=3,timeout=30,sleep_time=3):
    while 1:
        if retry <= 0:
            break
        try:
            con = urllib2.urlopen(url,data=data,timeout=timeout).read()
            return con
        except:
            time.sleep(sleep_time)
            retry -= 1
    


def remove_ankang_content_garbage(unicode_txt):
    '''
    >>> txt = '<div>共2页 上一页 1 2 下一页</div>'.decode('utf8')
    >>> remove_ankang_content_garbage(txt)
    u''
    >>> txt = '<div>  共2页<a>  上一页  </a>  1  <a>  2  </a><a>  下一页  </a>   </div>'.decode('utf8')
    >>> remove_ankang_content_garbage(txt)
    u''
    >>> txt = '<div><!-- 广告位：WZ336x280NR -->  <div>&nbsp;</div></table>  </div>'.decode('utf8')
    >>> remove_ankang_content_garbage(txt)
    u''
    
    '''
    
    
#     ankang_tag = 'ankangwang'
    ptns_garbage = [
                  re.compile(u'<div>\s*<!-- 广告位.*?</table>\s*</div>',re.DOTALL),
                  re.compile(u'<div>\s*共\d+页\s*(?:<[^>]+>)*\s*上一页.*?下一页\s*(?:<[^>]+>)*\s*</div>',re.DOTALL),
                  re.compile(u'(?:<[^>]+>)*\s*安\s*(?:<[^>]+>)*\s*康\s*[^网]*网\s*(?:<[^>]+>)*'),
                  ]
    
    for ptn in ptns_garbage:
        unicode_txt = ptn.sub('',unicode_txt)
#     unicode_txt = unicode_txt.replace(ankang_tag,'jinbangqm')
    return unicode_txt
    
    


def url_parse(url):
    def _get_query_dict(query_str):
        query_dict = {}
        for item in query_str.split('&'):
            kv_list = item.split('=')
            if len(kv_list) == 2:
                k,v = kv_list
                query_dict[k] = v
        return query_dict

    upo = urlparse.urlparse(url)
    path = upo.path
    query_str = upo.query
    query_dict = _get_query_dict(query_str)
    return path,query_dict    


def get_img_srcs(content):
    '''
    >>> content = '<html><img width="500" src="a.gif"><a href="/"></a> <img width="500" src="/b.gif"></html>'
    >>> get_img_srcs(content)
    ['a.gif', '/b.gif']
    >>> content = ''
    >>> get_img_srcs(content)
    []
    '''
    ptn = re.compile('''<img[^>]*src=['"]*([^'"]+)''')
    return ptn.findall(content)
    

if __name__ == '__main__':
    import doctest
    print doctest.testmod()
#     path = 'e:/a/b.html'
#     fp = open(path)
#     con = fp.read()
#     fp.close()
#     con = con.decode('cp936')
#     print con
#     print remove_ankang_content_garbage(con)
#     get_dir_by_fpath(path)
#     print is_string(None)
#     assert force_unicode(u'[1]人工流量：Javascript跳转测试 0.5-1'.encode('cp936')) == u'[1]人工流量：Javascript跳转测试 0.5-1'
#     print [remove_space('aaa aad ad\r\ncc aaa')]
#     print convert2encoding(r"D:\workspace\casper\test_src.html", "utf8", "cp936")
#     print [force_unicode('李强')]
#     txt = "<a href='www.baidu.com'>a</a>"
#     print remove_links(txt)
