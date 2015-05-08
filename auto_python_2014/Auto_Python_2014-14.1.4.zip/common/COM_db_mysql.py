'''
Created on 2014-12-12

@author: zhangziteng
'''

import MySQLdb
import os
import sys
import itertools

import MySQLdb.constants
import MySQLdb.converters
import MySQLdb.cursors

import hashlib

from COM_util_trans import Trans

#reload(sys)
#sys.setdefaultencoding('utf-8')

class COM_createdbconnection(object):
    '''
        create a database connection
    '''
    def __init__(self,host="172.30.100.12",user="qatest",password="qatest",dbname="qatest",port=3388,charset='utf8'):
        self.charset=charset
        self.comdbconncetion = MySQLdb.connect(host=host,user=user,passwd=password,db=dbname,port=port,charset=charset)
        self._cursor = self.comdbconncetion.cursor()
        self.trans = Trans()
    
    def get_collist(self,tbname):
        try:
            sql="select * from "+tbname+" where isRun=\'yes\' order by sn"
            cursor = self._cursor
            cursor.execute(sql)
            results = cursor.fetchall()
            col_name_list = [tuple[0] for tuple in cursor.description]  
            #print col_name_list
            #print results
            return col_name_list
        except:
            print "Error: unable to fecth data"
        #finally:
            #cursor.close()
    def get_query_data(self,tbname):
        try:
            sql="select * from "+tbname+" where isRun=\'yes\' order by sn"
            cursor = self._cursor
            cursor.execute(sql)
            col_name_list = [d[0] for d in cursor.description]
            #create dictionary for query data every col in each row
            return [Rower(itertools.izip(col_name_list, row)) for row in cursor]
        except:
            print "Error"
        #finally:
            #cursor.close()
    def get_query_data_custome(self,sql):
        try:
            #sql="select * from "+tbname+" where isRun=\'yes\' order by sn"
            cursor = self._cursor
            cursor.execute(sql)
            col_name_list = [d[0] for d in cursor.description]

            return [Rower(itertools.izip(col_name_list, row)) for row in cursor]
        except:
            print "Error"

    def get_query_collist_custome(self,sql):
        try:
            #sql="select * from "+tbname+" where isRun=\'yes\' order by sn"
            cursor = self._cursor
            cursor.execute(sql)
            col_name_list = [d[0] for d in cursor.description]

            return col_name_list
        except:
            print "Error"

    def get_query_collist_custome_sort(self,col_name_list,filterlist):
        try:
            col_name_list = sorted(col_name_list)
            for ft in filterlist:
                col_name_list.remove(ft)
            return col_name_list
        except:
            print "Error"

    def get_query_MD5(self,sortcollist,querydata,password):
        try:
            signstr=''
            dictquerydata = dict(querydata)
            for ky in sortcollist:
                #print "**************************"
                #print dictquerydata[ky]
                signstr = signstr+ky+str(dictquerydata[ky])
            signstr = signstr+password
            #print signstr
            m=hashlib.md5()
            m.update(signstr)
            md5signstr=m.hexdigest()
            #print md5signstr.upper()
            querydata.setdefault('sign',md5signstr.upper())
            #print type(querydata)
            #print querydata
            #print str(querydata)
            return querydata
        except:
            print "Error"


    def get_query_counts(self,tbname):
        try:
            sql="select * from "+tbname+" where isRun=\'yes\' order by sn"
            cursor = self._cursor
            cursor.execute(sql)
            tblist =[]
            i=0
            #querycounts =
            #print cursor.rowcount
            while i < cursor.rowcount:
                #print i
                tmptbarray = (tbname,i)
                #print tmptbarray
                tblist.append(tmptbarray)
                #print tblist
                #tbdict = self.trans.dictAdd(tbdict, tmptbdict)
                i+=1
            return tblist
        except:
            print "Error"
    
    def get_query_sn(self,tbname,username):
        try:
            #sql="select * from "+tbname+" where isRun=\'yes\' order by sn"
            casename="test"+tbname
            sql="SELECT b.* FROM "+tbname+" a, view_casesets_users_data b WHERE a.sn=b.casedataNo AND b.casename=\""+casename+"\" and b.username=\""+username+"\""
            #print sql
            cursor = self._cursor
            cursor.execute(sql)
            #print cursor
            tblist =[]
            col_name_list = [d[0] for d in cursor.description]
            tunknown = [Rower(itertools.izip(col_name_list, row)) for row in cursor]
            #print tunknown
            for item in tunknown:
                #print item["sn"]
                tmptbarray = (tbname,str(item["casedataNo"]))
                #print tmptbarray
                #print item
                #print item["sn"]
                tblist.append(tmptbarray)
            #querycounts =
            return tblist
        except:
            print "Error"

    def get_mobilequery_sn(self,tbname):
        try:
            #sql="select * from "+tbname+" where isRun=\'yes\' order by sn"
            casename="test"+tbname
            sql="SELECT \""+tbname+"\" as apiname,a.* FROM "+tbname+" a"
            print sql
            cursor = self._cursor
            cursor.execute(sql)
            print cursor
            tblist =[]
            col_name_list = [d[0] for d in cursor.description]
            tunknown = [Rower(itertools.izip(col_name_list, row)) for row in cursor]
            print tunknown
            for item in tunknown:
                #print item["sn"]
                tmptbarray = (tbname,str(item["sn"]))
                #print tmptbarray
                #print item
                #print item["sn"]
                tblist.append(tmptbarray)
            #querycounts =
            #print tblist
            return tblist
        except:
            print "Error"

    def get_query_distinct(self,tbname,colname):
        try:
            sql="select distinct "+colname+" as "+colname+" from "+tbname
            #print sql
            cursor = self._cursor
            cursor.execute(sql)
            #print cursor
            tblist =[]
            col_name_list = [d[0] for d in cursor.description]
            tunknown = [Rower(itertools.izip(col_name_list, row)) for row in cursor]
            #print tunknown
            for item in tunknown:
                #print item["sn"]
                tmptbarray = (str(item[colname]))
                #print tmptbarray
                #print item
                #print item["sn"]
                tblist.append(tmptbarray)
            #querycounts =
            return tblist
        except:
            print "Error"



    def get_query_rowindex(self,tbname,rowindex):
        try:
            sql="select * from "+tbname+" where sn="+rowindex+" order by sn"
            #print sql
            cursor = self._cursor
            cursor.execute(sql)
            #cursor.scroll(rowindex)
            results = cursor.fetchone()
            col_name_list = [d[0] for d in cursor.description]
            #trans None to u'NULL'
            listresults = list(results)
            listlen = len(listresults)
            i=0
            while i<listlen:
                if listresults[i] is None:
                    listresults[i] = u''
                i+=1
            results = tuple(listresults)
            return [Rower(itertools.izip(col_name_list, results))]
        except:
            print "get_query_rowindex Error"
        #finally:
            #cursor.close()
    def get_query_requestdata_except(self,tbname,rowindex,filterlist):
        try:
            sql="select * from "+tbname+" where sn="+rowindex+" order by sn"
            #print sql
            cursor = self._cursor
            cursor.execute(sql)
            #cursor.scroll(rowindex)
            results = cursor.fetchone()
            #print results
            col_name_list = [d[0] for d in cursor.description]
            listresults = list(results)
            listlen = len(listresults)
            i=0
            while i<listlen:
                if listresults[i] is None:
                    listresults[i] = u''
                i+=1
            results = tuple(listresults)
            
            requestdata=(Rower(itertools.izip(col_name_list, results)))
            for key in filterlist:
                del requestdata[key]
            return requestdata
        except:
            print "Error"
    
    def get_query_requestdata_include(self,tbname,rowindex,filterlist):
        try:
            sql="select * from "+tbname+" where sn="+rowindex+" order by sn"
            cursor = self._cursor
            cursor.execute(sql)
            #cursor.scroll(rowindex)
            results = cursor.fetchone()
            #print results
            col_name_list = [d[0] for d in cursor.description]
            temp_list=[]
            for ll in col_name_list:
                count=0
                for filter in filterlist:
                    if ll==filter:
                        count=1
                if count==0 :
                    temp_list.append(ll) 
                    
            #print 'iiiiiiiiiiiiiii',temp_list
            #return [Rower(itertools.izip(col_name_list, row)) for row in cursor]
            #return [Rower(itertools.izip(col_name_list, results))]
            requestdata=(Rower(itertools.izip(col_name_list, results)))
            for key in temp_list:
                del requestdata[key]
            return requestdata
        except:
            print "Error"
    
    def get_query_reconstruct(self,olddict,newdict):
        newrequest=self.trans.dictAdd(olddict, newdict)
        return newrequest


            
    def close(self):
        self._cursor.close()
        self.comdbconncetion.close()

class Rower(dict):
    """A dict that allows for object-like property access syntax."""
    #print '%%%%%%%%%%%%%%%%%%%%%%%%%%%in Rower'
    def __getattr__(self, name):
        try:
            print '-----------------',self[name]
            return self[name]
        except KeyError:
            raise AttributeError(name)


if __name__ == '__main__':
    db = COM_createdbconnection("172.30.100.12","qatest","qatest","qatest",3388,'gbk')
    sql="select * from dh_item_get_20"
    #db = COM_createdbconnection()
    #newdict={"aaa":1111,"bbb":2222}
    #print db.get_collist("dh_item_get_20")
    #db.get_query_data("dh_item_get_20")
    #print db.get_query_data("dh_item_get_20")
    #tbunknown = db.get_query_data("dh_item_get_20")

    print "begin"
    newsql = "select * from dhnew_items_get"
    #coldict = db.get_query_data_custome(newsql)
    querydata = db.get_query_requestdata_except("dhnew_items_get","1",["sn","check_JSON"])
    collist = db.get_query_collist_custome(newsql)
    sortcollist = db.get_query_collist_custome_sort(collist,["sn","check_JSON"])
    print sortcollist
    finaldata = db.get_query_MD5(sortcollist,querydata,"L5U8R6X0")
    print finaldata
    print type(finaldata)
    db.get_mobilequery_sn("dhnew_items_get")
    #db.close()

    print "end"
    '''
    newsql="select * from dhnew_items_get"
    coldict = db.get_query_data_custome(newsql)
    print coldict

    testfilter = db.get_query_requestdata_except("dhnew_items_get","1",["sn","check_JSON"])

    print type(coldict)
    del coldict[0]['sn']
    print coldict

    coldictfilter = testfilter
    coldictfilter = dict(coldictfilter)
    print coldictfilter
    print type(coldictfilter)

    collist = db.get_query_collist_custome(newsql)
    print collist
    collist.remove('sn')
    collist.remove('check_JSON')
    print collist

    sortedcollist = sorted(collist)
    print sortedcollist
    signstring=''
    for ky in sortedcollist:
        print "**************************"
        print coldictfilter[ky]
        signstring=signstring+ky+str(coldictfilter[ky])
    signstring=signstring+'L5U8R6X0'
    print signstring
    m=hashlib.md5()
    m.update(signstring)
    md5signstring=m.hexdigest()
    print md5signstring.upper()
    testfilter.setdefault('sign',md5signstring.upper())
    print testfilter
    print str(testfilter)

    #for item in tbunknown:
     #   print item
      #  print item["sn"]
    #print db.get_query_sn("dh_item_get_20")

    print '^^^',db.get_query_rowindex("dh_item_get_20","1")
    tlist = db.get_query_rowindex("dh_item_get_20","1")
    print tlist
    db.get_query_counts("dh_item_get_20")
    print db.get_query_counts("dh_item_get_20")
    for item in tlist:
        print '^^^^^',item['chck_JSON']
    print"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
    print db.get_query_sn("dh_item_get_20","huohui")
    print "$$$$$$$$$$$$$$$$$$"
    print db.get_query_distinct("view_casesets_users_data","username")
    #print db._cursor
    #print '~~~~~',db.get_query_requestdata(sql, 0)
#    print '~~~~~',db.get_query_requestdata_except("dh_item_get_20", 0,['username','password'])
#    print '=====',db.get_query_requestdata_include("dh_item_get_20", 0,['username','password'])
#    trequest=db.get_query_requestdata_include("dh_item_get_20", 0,['username','password'])
#    print trequest
#    print trequest['username']
#    print '+++++',db.get_query_reconstruct(db.get_query_requestdata_include("dh_item_get_20", 0,['username','password']), newdict)
    '''
#    db.close()