#coding=utf-8
'''
Created on 2014-12-16

@author: zhangziteng
'''
#import unittest
import common
from common.COM_db_mysql import COM_createdbconnection
from common.COM_httpclient import COM_postrequest
from init.init_value import init_value
from common.COM_util_trans import Trans


class APIrequest(COM_createdbconnection,COM_postrequest):
    def cpt_setusername(self,username):
        self.username=username

    def cpt_createdbconnection(self):
        self.dbconnection = COM_createdbconnection()
        
    def cpt_createdbconnection_given(self,host,dbname,user,password):
        self.dbconnection = COM_createdbconnection(host,dbname,user,password)
    
    def cpt_getcolumlist(self,tbname):
        self.columlist = self.dbconnection.get_collist(tbname)

    def cpt_mobilegetcolumlist(self,sql):
        self.columlist = self.dbconnection.get_query_collist_custome(sql)
    
    def cpt_getrow(self,tbname,rowindex):
        self.row = self.dbconnection.get_query_rowindex(tbname, rowindex)
    
    def cpt_getall(self,tbname):
        self.results = self.dbconnection.get_query_data(tbname)
    
    def cpt_getcounts(self,tbname):
        self.counts = self.dbconnection.get_query_counts(tbname)
    
    def cpt_getsn(self,tbname,username):
        self.sn = self.dbconnection.get_query_sn(tbname,username)

    def cpt_getmobilesn(self,tbname):
        self.sn = self.dbconnection.get_mobilequery_sn(tbname)
            
    def cpt_getusers(self):
        self.users = self.dbconnection.get_query_distinct("view_casesets_users_data","username")
    #def cpt_getsn(self,tbname):
     #   self.snlist = self.dbconnection.

    def cpt_getapinames(self):
        self.apinames = self.dbconnection.get_query_distinct("view_mobileapi_name","table_name")

    def cpt_getusersnew(self,user):
        self.users = self.dbconnection.get_query_distinct("view_casesets_users_data","username")

    def cpt_getpostdata(self,tbname,rowindex,filterlist):
        self.requestdata = self.dbconnection.get_query_requestdata_include(tbname,rowindex,filterlist)
    
    def cpt_getpostdata_filter(self,tbname,rowindex,filterlist):
        self.requestdata = self.dbconnection.get_query_requestdata_except(tbname,rowindex,filterlist)
    
    def cpt_createhttpconnection(self,url):
        self.httpconnection = COM_postrequest(url)
    
    def cpt_sendhttprequest(self,path,requestdata):
        self.response = self.httpconnection.post(path, requestdata)
    
    def cpt_sendhttprequestreturnorderstr(self,path,requestdata):
        self.response = self.httpconnection.postreturstronorder(path, requestdata)

    def cpt_sendhttprequestmobile(self,path,requestdata):
        self.response = self.httpconnection.mobilepost(path, requestdata)

    def cpt_responseformattojson(self,response):
        self.dictdecoderesponse=self.trans.dictTojson(response)
        #self.dictdecode={k.decode("utf8",'ignore'):v.decode("utf8",'ignore') for k,v in self.response.items()}
        #print json.dumps(self.response, encoding='UTF-8', ensure_ascii=False)
    def cpt_responseformattojsonstr(self,response):
        self.dictdecoderesponsestr=str(self.trans.unicodeToStr(response))
        
    def cpt_requestformattojson(self,request):
        self.dictdecoderequest=self.trans.dictTojson(request)

    def cpt_pickpostdatafromresponse(self,key):
        self.dict =self.httpconnection.responsefilter(key)   
        
    def cpt_reconstructrequest(self,olddict,plusdict):
        self.requestdata = self.trans.dictAdd(olddict, plusdict)
    
    def cpt_strreplace(self,find,replace):
        self.dictdecoderesponsestr=self.trans.strreplace(self.dictdecoderesponsestr, find, replace)

    def cpt_sort_collist_custome(self,filterlist):
        self.sortcollist = self.dbconnection.get_query_collist_custome_sort(self.columlist,filterlist)

    def cpt_dosign(self,password):
        self.querydosign = self.dbconnection.get_query_MD5(self.sortcollist,self.requestdata,password)
    
    def cpt_close(self):
        self.dbconnection.close()
    
    def cpt_api_getresponse(self,tbname,rowindex):
        #apitest = TestCase()
        #tbname="dh_item_get_20"
        init=init_value()
        self.cpt_createdbconnection()
        self.cpt_getcolumlist(tbname)
        #print self.columlist
        self.cpt_getrow(tbname, rowindex)
        #print self.row
        self.cpt_getpostdata(tbname, rowindex, init.include)
        self.cpt_createhttpconnection(init.url)
        # 
        self.cpt_sendhttprequest(init.path, self.requestdata)
        # '###get token #################'
        self.cpt_pickpostdatafromresponse(init.token)
        # get the api private request data
        self.cpt_getpostdata_filter(tbname, rowindex, init.filter)
        # reconstruct the request add timestamp and access_token
        self.cpt_reconstructrequest(self.requestdata, self.dict)
        # send request and order loads the response to json str
        self.cpt_sendhttprequestreturnorderstr(init.path_v, self.requestdata)
        # format fake unicode str to str for assertequal
        self.cpt_responseformattojsonstr(self.response)
        self.cpt_getpostdata(tbname, rowindex, init.chck)
        self.chck=self.requestdata[init.chck[0]]
        #self.assertEqual(self.requestdata[init.chck[0]],self.dictdecoderesponse,"expect is "+self.requestdata[init.chck[0]]+ "but actual is "+self.dictdecoderesponse)
        self.cpt_close()

    def cpt_mobileapi_getresponse(self,tbname,rowindex):
        tran = Trans()
        init=init_value()
        sql = "select * from "+tbname
        self.cpt_createdbconnection()
        self.cpt_mobilegetcolumlist(sql)
        #print self.columlist
        self.cpt_sort_collist_custome(init.mobilefilter)
        #print self.sortcollist
        self.cpt_getrow(tbname, rowindex)
        print "********"
        print self.row
        self.chck=self.row[0][init.chck[0]]
        #self.chck=tran.jsonToStrOrder(self.chck)
        #print '**********'+self.chck
        #print type(self.chck)
        self.cpt_getpostdata_filter(tbname,rowindex,init.mobilefilter)
        self.cpt_dosign(init.mobilepassword)
        self.cpt_createhttpconnection(init.mobileurl)
        self.cpt_sendhttprequestreturnorderstr(init.mobilepath, self.querydosign)
        self.cpt_responseformattojsonstr(self.response)
        #print self.dictdecoderesponsestr
        '''
        print self.response
        #print str(self.response)
        print type(self.response)
        print "-------"
        print self.chck
        print type(self.chck)
        chckstr=self.chck
        print type(chckstr)
        print chckstr
        res = self.response
        chckstr = tran.jsonToStrOrder(chckstr)
        print chckstr
        print type(chckstr)
        print "||||||||||||"
        print res
        resnew = str(res).replace("\r\n","")
        #resnew = res.replace("\r\n","")
        print resnew
        print cmp(chckstr,res)
        print (chckstr == res)
        #self.cpt_responseformattojsonstr(self.response)
        #print self.dictdecoderesponsestr
        #print type(self.dictdecoderesponsestr)
        #print type(str(self.dictdecoderesponsestr))
        #print type(self.dictdecoderesponsestr)
        #print type(self.chck)
        '''
        self.cpt_close()
    
'''
if __name__ == '__main__':
    #sql="select * from dh_item_get_20"
    """
    sql="dh_item_get_20"
    include=['grant_type','username','password','client_id','client_secret','scope']
    filter=['sn','isRun','flag','grant_type','username','password','client_id','client_secret','scope','chck_JSON','chck_JSONMD5']
    url="api.dhgate.com"
    path="/dop/oauth2/access_token?"
    key="access_token"
    path_v="/dop/router"
    """
    tapirequest = APIrequest()
    tapirequest.cpt_mobileapi_getresponse("dhnew_items_get","1")

    #tapi = APIrequest()
    #tapi.cpt_createdbconnection()
    #tapi.cpt_getapinames()
    #print tapi.apinames
    print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"


    """
    tapirequest = APIrequest()
    tapirequest.cpt_createdbconnection()
    print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
    tapirequest.cpt_getcolumlist(sql)
    print tapirequest.columlist
    tapirequest.cpt_getrow(sql, "1")
    print tapirequest.row
    tapirequest.cpt_getpostdata(sql, "1", include)
    print tapirequest.requestdata
    #print type(tapirequest.requestdata)
    tapirequest.cpt_createhttpconnection(url)
    tapirequest.cpt_sendhttprequest(path, tapirequest.requestdata)
    print tapirequest.response
    print '###get token #################'
    tapirequest.cpt_pickpostdatafromresponse(key)
    print tapirequest.dict
    print '###send request'
    tapirequest.cpt_getpostdata_filter(sql, "1", filter)
    print tapirequest.requestdata
    #tapirequest.cpt_reconstructresponse(tapirequest.requestdata, tapirequest.dict)
    #print tapirequest.requestdata
    #tapirequest.cpt_sendhttprequest(path_v, tapirequest.requestdata)
    #print type(tapirequest.response)
    #print tapirequest.response
    #tapirequest.cpt_responseformattojson(tapirequest.response)
    print"88888888888888888"
    tapirequest.cpt_getsn("dh_item_get_20")
    print tapirequest.snlist
    #print '****'
    #print tapirequest.dictdecode
    #print tapirequest.requestdata
    #print tapirequest.response["message"]
    #print tapirequest.response["solution"]
    #print type(tapirequest.response["solution"].encode('gbk'))
    """
    #print str(tapirequest.response)
    print '#################'
    
'''
    
    
    