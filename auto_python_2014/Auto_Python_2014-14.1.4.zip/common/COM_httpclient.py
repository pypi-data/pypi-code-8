'''
Created on 2014-12-15

@author: zhangziteng
'''
import httplib
import urllib
from COM_util_trans import Trans
from COM_util_tools import COM_tools

class COM_postrequest(object):
    '''
    classdocs
    '''
    def __init__(self,url,header={"Content-Type":"application/x-www-form-urlencoded","Connection":"Keep-Alive"}):
        self.url=url
        self.method='POST'      
        self.header=header  
        self.trans=Trans()
        self.tools=COM_tools()
        self.dict={}

    '''
    return an dict type json
    '''
    def post(self,path,param):
        data=urllib.urlencode(param)
        try:
            conn=httplib.HTTPConnection(self.url)
            conn.request(self.method, path, data,self.header)
            response=conn.getresponse()
            responseread = response.read()
            responseread = responseread.replace("&amp;", "&")
            print responseread
            self.response = self.trans.jsonTodict(responseread)
            #print "**********^^^^",self.response
            return self.response
        except:
            print "Error"

    def mobilepost(self,path,param):
        data=urllib.urlencode(param)
        try:
            conn=httplib.HTTPConnection(self.url)
            conn.request(self.method, path, data,self.header)
            mobileresponse=conn.getresponse()
            mobileresponseread = mobileresponse.read()
            mobileresponseread = mobileresponseread.replace("&amp;", "&")
            print mobileresponseread
            #self.mobileresponse = self.trans.jsonTodict(mobileresponseread)
            self.mobileresponse = mobileresponseread
            #print "**********^^^^",self.response
            return self.mobileresponse
        except:
            print "Error"
    '''
    return an order jsonstr
    '''
    def postreturstronorder(self,path,param):
        data=urllib.urlencode(param)
        try:
            conn=httplib.HTTPConnection(self.url)
            conn.request(self.method, path, data,self.header)
            response=conn.getresponse()
            responseread = response.read()

            responseread = responseread.strip("\r\n")

            self.response = self.trans.jsonToStrOrder(responseread)
            return self.response
        except:
            print "Error"

    def responsefilter(self,key):
        timestamp=self.tools.get_timestamp()
        timedict=self.trans.dictcreate("timestamp", timestamp)
        val=self.response[key]
        newdict=self.trans.dictcreate(key, val)
        self.dict=self.trans.dictAdd(self.dict, newdict)
        self.dict=self.trans.dictAdd(self.dict, timedict)
        return self.dict
    
    def responseformatjson(self,response):
        self.responsejsonstr=self.trans.dictTojson(response)
        return self.responsejsonstr
            

if __name__ == '__main__':
    params={'grant_type':'password','username':'zzt001','password':'test4321','client_id':'H72EAAUnEP','client_secret':'42a8d883faba4dd4b53cc4471c06ea8e','scope':'basic'}
    #dopost = Postrequest("http://www.dhpay.com/dop/oauth2/access_token?",{"Content-Type":"application/x-www-form-urlencoded","Connection":"Keep-Alive"})
    dopost = COM_postrequest("api.dhgate.com",{"Content-Type":"application/x-www-form-urlencoded","Connection":"Keep-Alive"})
    #print dopost.post("/dop/oauth2/access_token?", params)
    #print dopost.response['access_token']
    #print dopost.responsefilter('access_token')
    #print dopost.responsefilter('scope')
        #print dopost.responsereconstruct(dopost.newdict)
        #print dopost.post(params)
    params={'method': u'dhnew.Items.Get','page_size': u'10', 'order_by': 'price:asc', 'cid': '', 'format': 'JSON', 'app_key': 'E9DA9D6E', 'v': '1.1', 'query': 'test', 'page_no': '1','sign':'965E37591B923A05116788254350034C'}
    dopostnew = COM_postrequest("192.168.222.114",{"Content-Type":"application/x-www-form-urlencoded","Connection":"Keep-Alive"})
    print dopostnew.mobilepost("/apiWeb/mobileapp.do?", params)
    print type(dopostnew.mobilepost("/apiWeb/mobileapp.do?", params))
    #rsold=dopostnew.mobilepost("/apiWeb/mobileapp.do?", params)
    #print dopostnew.responseformatjson(rsold)