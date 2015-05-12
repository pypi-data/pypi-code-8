'''
Created on 03 19, 2015

@author: tolerious

'''
from django.db import models
from models import *
import requests,json,logging,pprint

class Department(models.Model):
    name = models.CharField(max_length="100",default="")
    parentid = models.IntegerField(default=1)
    order = models.IntegerField(default=1)
    department_id = models.IntegerField(default=-1)
    error_code = models.CharField(max_length=200,default="")
    error_msg = models.CharField(max_length=200,default="")

    class Meta:
        app_label = "app"

    def __unicode__(self):
        return self.name + ";" + str(self.department_id)

    def create_department(self):
        dic = {
            "name":self.name,
            "parentid":self.parentid,
            "order":self.order,
        }
        accesstoken = AccessToken.objects.get(id=1).get_access_token()
        url = "https://qyapi.weixin.qq.com/cgi-bin/department/create?access_token=" + accesstoken
        data = json.dumps(dic)
        r = requests.post(url,data=data)
        return_dic = r.json()
        logging.info(return_dic)
        if int(return_dic.get("errcode")) == 0:
            ids = return_dic["id"]
            self.department_id = ids
            self.error_code = return_dic["errcode"]
            self.error_msg = return_dic["errmsg"]
            self.save()
            return True
        else:
            self.department_id = -2
            self.error_code = return_dic["errcode"]
            self.error_msg = return_dic["errmsg"]
            self.save()
            return False

    def update_department(self):
        dic = {
            "id": self.department_id,
            "name": self.name,
            "parentid":self.parentid,
            "order":self.order

        }
        accesstoken = AccessToken.objects.get(id=1).get_access_token()
        url = "https://qyapi.weixin.qq.com/cgi-bin/department/update?access_token=" + accesstoken
        data = json.dumps(dic)
        r = requests.post(url,data=data)
        return_dic = r.json()
        logging.info(return_dic)
        if int(return_dic.get("errcode")) == 0:
            self.save()
            self.error_code = return_dic['errcode']
            self.error_msg = return_dic['errmsg']
            return True
        else:
            self.error_code = return_dic['errcode']
            self.error_msg = return_dic['errmsg']
            return False

    def delete_department(self):
        accesstoken = AccessToken.objects.get(id=1).get_access_token()
        url = "https://qyapi.weixin.qq.com/cgi-bin/department/delete?access_token=" + accesstoken + "&id=" + str(self.department_id)
        r = requests.get(url)
        return_dic = r.json()
        logging.info(return_dic)
        self.error_code = return_dic['errcode']
        self.error_msg = return_dic['errmsg']
        if int(return_dic.get("errcode")) == 0:
            return True
        else:
            return False

    def get_department_list(self):
        accesstoken = AccessToken.objects.get(id=1).get_access_token()
        url = "https://qyapi.weixin.qq.com/cgi-bin/department/list?access_token=" + accesstoken + "&id=" + str(self.department_id)
        r = requests.get(url)
        return_dic = r.json()
        logging.info(return_dic)
        return return_dic

class Employee(models.Model):
    userid = models.CharField(default="",max_length=100,blank=False)
    name = models.CharField(default="",blank=False,max_length=100)
    department_list = models.CharField(default="[1]", blank=True,max_length=500)
    position = models.CharField(default="", max_length=100)
    mobile = models.CharField(default="",max_length=100)
    email = models.CharField(default="",max_length=100)
    weixinid = models.CharField(default="",max_length=100)
    extattr = models.CharField(default='{"attrs":[]}', blank=True,max_length=500)
    error_code = models.CharField(max_length=10,default="")
    error_msg = models.CharField(max_length=100,default="")

    class Meta:
        app_label = "app"

    def __unicode__(self):
        return self.userid + ";" + self.weixinid

    def create_member(self):
        access_token = AccessToken.objects.get(id=1).get_access_token()
        url = "https://qyapi.weixin.qq.com/cgi-bin/user/create?access_token=" + access_token
        dump_department_list = json.loads(self.department_list)
        print self.extattr
        exta_dic = json.loads(self.extattr)
        if self.mobile == self.email == self.weixinid == "":
            self.email = "xx@example.com"
        dic = {
            "userid": self.userid,
            "name": self.name,
            "department":dump_department_list,
            "position":self.position,
            "mobile":self.mobile,
            "email":self.email,
            "weixinid":self.weixinid,
            "extattr":exta_dic,
        }
        data = json.dumps(dic)
        r = requests.post(url,data=data)
        return_json = r.json()
        logging.info(return_json)
        self.error_code = return_json["errcode"]
        self.error_msg = return_json["errmsg"]
        self.save()
        if int(return_json.get("errcode")) == 0:
            return True
        else:
            return False

    def update_member(self):
        access_token = AccessToken.objects.get(id=1).get_access_token()
        url = "https://qyapi.weixin.qq.com/cgi-bin/user/update?access_token=" + access_token
        dump_department_list = json.loads(self.department_list)
        print self.extattr
        exta_dic = json.loads(self.extattr)
        dic = {
            "userid": self.userid,
            "name": self.name,
            "department":dump_department_list,
            "position":self.position,
            "mobile":self.mobile,
            "email":self.email,
            "weixinid":self.weixinid,
            "extattr":exta_dic,
        }
        data = json.dumps(dic)
        r = requests.post(url,data=data)
        return_json = r.json()
        logging.info(return_json)
        return return_json

    def delete_member(self):
        access_token = AccessToken.objects.get(id=1).get_access_token()
        url = "https://qyapi.weixin.qq.com/cgi-bin/user/delete?access_token=" + access_token + "&userid=" + str(self.userid)
        r = requests.get(url)
        return_json = r.json()
        logging.info(return_json)
        return return_json

    def delete_bulk_members(self,delete_list):
        access_token = AccessToken.objects.get(id=1).get_access_token()
        url = "https://qyapi.weixin.qq.com/cgi-bin/user/batchdelete?access_token=" + access_token
        dic = {
            "useridlist": delete_list
        }
        data = json.dumps(dic)
        r = requests.post(url,data=data)
        return_json = r.json()
        logging.info(return_json)
        return return_json

    def get_employee_info(self):
        access_token = AccessToken.objects.get(id=1).get_access_token()
        url = "https://qyapi.weixin.qq.com/cgi-bin/user/get?access_token=" + access_token + "&userid=" + self.userid

        r = requests.get(url)
        return_json = r.json()
        logging.info(return_json)
        return return_json

    # may need to improve
    def get_department_employee_info(self,department_id,fetch_child="1",status="0"):
        access_token = AccessToken.objects.get(id=1).get_access_token()
        url = "https://qyapi.weixin.qq.com/cgi-bin/user/simplelist?access_token="+ access_token +"&department_id=" + str(department_id) + "&fetch_child="+ fetch_child+ "&status=" + status
        r = requests.get(url)
        return_json = r.json()
        logging.info(return_json)
        return return_json

    def get_department_employee_deatil_info(self,department_id,fetch_child="1",status="0"):
        pass