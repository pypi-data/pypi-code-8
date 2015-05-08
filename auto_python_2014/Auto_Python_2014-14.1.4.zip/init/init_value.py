'''
Created on 2014-12-17

@author: zhangziteng
'''
class init_value(object):
    def __init__(self):
        #self.sql="select * from dh_item_get_20"
        self.include=['grant_type','username','password','client_id','client_secret','scope']
        self.filter=['sn','isRun','flag','grant_type','username','password','client_id','client_secret','scope','chck_JSON','chck_JSONMD5']
        self.chck=['chck_JSON']
        self.url="api.dhgate.com"
        self.path="/dop/oauth2/access_token?"
        self.token="access_token"
        self.path_v="/dop/router"

        self.mobileinclude=[]
        self.mobilefilter=['sn','chck_JSON']
        self.mobileurl="192.168.222.114"
        self.mobilepath="/apiWeb/mobileapp.do?"
        self.mobilepassword="L5U8R6X0"

if __name__ == '__main__':
    pass