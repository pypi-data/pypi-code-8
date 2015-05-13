'''
Created on 2014-12-29

@author: zhangziteng
'''
import common
from common.COM_db_mysql import COM_createdbconnection
from init.init_value import init_value

class Drivergetcase(COM_createdbconnection):
    #def __init__(self, username="admin"):
     #   self.username=username
    def cpt_setUsername(self,username="admin"):
        self.username=username
    
    def cpt_createdbconnection(self):
        self.dbconnection = COM_createdbconnection()
        
    def cpt_createdbconnection_given(self,host,dbname,user,password):
        self.dbconnection = COM_createdbconnection(host,dbname,user,password)
    
    def cpt_getcolumlist(self,tbname):
        self.columlist = self.dbconnection.get_collist(tbname)
    
    def cpt_getrow(self,tbname,rowindex):
        self.row = self.dbconnection.get_query_rowindex(tbname, rowindex)
    
    def cpt_getcases(self):
        if self.username=='admin':
            sql="select * from view_casesets_api"
            self.results = self.dbconnection.get_query_data_custome(sql)
        else:
            #print self.username
            username=str(self.username)
            sql="select * from view_casesets_users where username=\""+username+"\""
            #print sql
            #sql="select * from view_casesets_users where username=\"zhangziteng\""
            self.results = self.dbconnection.get_query_data_custome(sql)

    def cpt_getcases_mobile(self):
        #print self.username
        username=str(self.username)
        sql="select * from "+username
        print "========="
        print sql
        #sql="select * from view_casesets_users where username=\"zhangziteng\""
        self.results = self.dbconnection.get_query_distinct(username,"api")


    def cpt_getcases_mobile_data(self):
        #print self.username
        username=str(self.username)
        sql="select * from "+username+""
        #print sql
        #sql="select * from view_casesets_users where username=\"zhangziteng\""
        self.resultsdata = self.dbconnection.get_query_data_custome(sql)
    
    def cpt_getcases_data(self):
        if self.username=='admin':
            sql="select * from view_casesets_users_data where username=\"admin\""
            self.resultsdata = self.dbconnection.get_query_data_custome(sql)
        else:
            #print self.username
            username=str(self.username)
            sql="select * from view_casesets_users_data where username=\""+username+"\""
            #print sql
            #sql="select * from view_casesets_users where username=\"zhangziteng\""
            self.resultsdata = self.dbconnection.get_query_data_custome(sql)

    
if __name__ == '__main__':
    tdrivergetcase=Drivergetcase()
    tdrivergetcase.cpt_createdbconnection()
    print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
    #tdrivergetcase.cpt_setUsername()
    tdrivergetcase.cpt_setUsername("zhangziteng")
    tdrivergetcase.cpt_getcases()
    print tdrivergetcase.results
    tdrivergetcase.cpt_getcases_data()
    print tdrivergetcase.resultsdata