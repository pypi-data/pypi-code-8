'''
Created on 2014-12-16

@author: zhangziteng
'''
import simplejson
import json
from json import *
from collections import OrderedDict


class Trans(object):
    def __init__(self):
        pass
    
    def jsonTodict(self,jsonstr):
        return simplejson.loads(jsonstr)
    
    # loads str on order to json str
    def jsonToStrOrder(self,jsonstr):
        tjsonstr = json.dumps(jsonstr,sort_keys=True,encoding='UTF-8',ensure_ascii=False)
        return tjsonstr
    
    # when occured the str like "\{\"status\":{\"code\":\"00000000\",\"message\":\"OK\"..."
    # the str type show the unicode but it isn't real unicode
    # should use json.loads trans it to the str type
    def unicodeToStr(self,jsonstr):
        tjsonstr = json.loads(jsonstr)
        return tjsonstr
    
    def dictTojson(self,dict):
        return json.dumps(dict, encoding='UTF-8', ensure_ascii=False)
        #return json.dumps(OrderedDict(dict, encoding='UTF-8', ensure_ascii=False))
    def strreplace(self,str,find,replace):
        replacestr = str.replace(find, replace)
        return replacestr
        
    def dictcreate(self,key,val):
        dict={key:val}
        return dict
    
    def dictAdd(self,olddict,newdict):
        olddict.update(newdict)
        return olddict

if __name__ == '__main__':
    trans=Trans()
    jsonstr="{\"expires_in\":1418810324775,\"scope\":\"basic\",\"refresh_token\":\"wrzJuUGRIXOKBG9bUiXMj0qIG5X8G3hGomYy1My5\",\"access_token\":\"vu1NoXUesmxA2IcOpLZGrhvPtL9fMsOh6Q02oGy1\"}"
    print type(simplejson.loads(jsonstr))
    print type(trans.jsonTodict(jsonstr))
    olddict = {"aaa":111,"bbb":222}
    newdict = {"ccc":333,"ddd":444}
    print trans.dictAdd(olddict, newdict)
    key="what"
    val="nothing"
    print trans.dictcreate(key, val)
    print trans.dictTojson(olddict)
    dictnn = {'chck_JSON': u'{"status":{"code":"00000000","message":"OK","solution":"","subErrors":[]},"siteId":"RU","itemCode":"151000779","supplierId":"ff8080813d8fe1cb013d902443340030","expireDate":"2015-02-02 16:43:57.0","catePubId":"011110103001","itemGroupId":"","shippingModelId":"ff8080813f3ce157013f3ce599b0000e","vaildDay":"90","itemBase":{"itemName":"\u041e\u043f\u0442\u043e\u0432\u0430\u044f - 2013 \u043d\u043e\u0432\u0443\u044e fashion2012 \u043e\u0441\u0435\u043d\u044c \u043d\u043e\u0432\u044b\u0445 \u0436\u0435\u043d\u0441\u043a\u0438\u0445 \u043a\u043e\u0441\u0442\u044e\u043c\u0430 \u043c\u043e\u0434\u044b \u043a\u043e\u0441\u0442\u044e\u043c \u041a\u0440\u0430\u0433\u0438 \u043f\u043e\u0434\u043b\u0438\u043d\u043d\u044b\u0435 \u0434\u0430\u043c\u044b \u043e\u0444\u0438\u0441 \u043d\u043e\u0441\u0438\u0442\u044c \u0443\u043d\u0438\u0444\u043e\u0440\u043c\u0443 817jiling","shortDesc":"Alibaba \u043e\u043f\u0442\u043e\u0432\u044b\u0435 \u0432\u044b\u0441\u043e\u043a\u043e\u0435 \u043a\u0430\u0447\u0435\u0441\u0442\u0432\u043e \u043d\u0430 \u0440\u044b\u043d\u043a\u0435 \u043d\u0438\u0437\u043a\u0430\u044f \u0437\u0430\u043a\u0443\u043f\u043e\u0447\u043d\u0430\u044f \u0446\u0435\u043d\u0430 2012 \u043e\u0441\u0435\u043d\u044c \u043c\u043e\u0434\u0430 \u043d\u043e\u0432\u044b\u0445 \u043c\u0443\u0436\u0447\u0438\u043d \u043a\u043e\u0441\u0442\u044e\u043c \u043a\u043e\u0441\u0442\u044e\u043c \u041a\u0440\u0430\u0433\u0438 \u043f\u043e\u0434\u043b\u0438\u043d\u043d\u044b\u0435 \u0434\u0430\u043c\u044b \u043e\u0444\u0438\u0441 \u043d\u043e\u0441\u0438\u0442\u044c \u0444\u043e\u0440\u043c\u0443 817, \u043f\u0440\u043e\u0444\u0435\u0441\u0441\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u044b\u0445 \u0436\u0435\u043d\u0449\u0438\u043d, \u0441\u043e\u0431\u0440\u0430\u043b\u0438\u0441\u044c \u0437\u0434\u0435\u0441\u044c \u0448\u0438\u0440\u043e\u043a\u0438\u0439 \u0441\u043f\u0435\u043a\u0442\u0440 \u043f\u043e\u0441\u0442\u0430\u0432\u0449\u0438\u043a\u043e\u0432, \u043f\u043e\u043a\u0443\u043f\u0430\u0442\u0435\u043b\u0435\u0439, \u043f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0438\u0442\u0435\u043b\u0435\u0439.\u042d\u0442\u043e 2012 \u043e\u0441\u0435\u043d\u044c \u043d\u043e\u0432\u044b\u0435 \u0436\u0435\u043d\u0441\u043a\u0438\u0435 \u043a\u043e\u0441\u0442\u044e\u043c \u043c\u043e\u0434\u044b \u043a\u043e\u0441\u0442\u044e\u043c \u041a\u0440\u0430\u0433\u0438 \u043f\u043e\u0434\u043b\u0438\u043d\u043d\u044b\u0435 \u0434\u0430\u043c\u044b \u043e\u0444\u0438\u0441 \u043d\u043e\u0441\u0438\u0442\u044c \u0443\u043d\u0438\u0444\u043e\u0440\u043c\u0443 817 \u043f\u043e\u0434\u0440\u043e\u0431\u043d\u043e\u0441\u0442\u0438 \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430.\u0426\u0432\u0435\u0442: \u0447\u0435\u0440\u043d\u044b\u0439, \u0418\u0441\u0442\u043e\u0447\u043d\u0438\u043a \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438: \u041e\u0431\u0435\u0434, \u041b\u0438\u0441\u0442\u0438\u043d\u0433 \u0413\u043e\u0434 / \u0421\u0435\u0437\u043e\u043d: 2013 \u041e\u0441\u0435\u043d\u044c, \u041c\u0430\u0440\u043a\u0435\u0442\u0438\u043d\u0433 \u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f: \u041d\u043e\u0432\u044b\u0439, \u041f\u0443\u043d\u043a\u0442: 8650, \u041f\u0440\u043e\u0438\u0441\u0445\u043e\u0436\u0434\u0435\u043d\u0438\u0435: \u0414\u0443\u043d\u0433\u0443\u0430\u043d\u044c, \u0431\u0443\u0434\u044c \u0438\u043d\u0432\u0435\u043d\u0442\u0430\u0440\u0438\u0437\u0430\u0446\u0438\u0438: \u0434\u0430, \u0435","htmlContent":null,"keyWord1":null,"keyWord2":null,"keyWord3":null,"videoUrl":null},"itemInventory":{"inventoryLocation":"CN","inventoryQty":3297,"inventoryOriQty":3304,"inventoryStatus":"1"},"itemPackage":{"grossWeight":1.0,"height":1.0,"length":1.0,"width":1.0,"measureId":"00000000000000000000000000000003","packingQuantity":1,"itemWeigthRange":null},"itemSaleSetting":{"leadingTime":2,"maxSaleQty":10000,"priceConfigType":null,"minWholesaleQty":1},"itemImgList":[{"imgUrl":"albu_248802830_00","imgMd5":"fafa5efeaf3cbe3b23b2748d13e629a1","type":0}],"itemAttrList":[{"isbrand":1,"itemAttrValList":null,"attrId":99,"attrName":"BRAND","attrNameCn":"\u54c1\u724c","prodAttrValList":[{"attrId":99,"attrName":"BRAND","attrValId":99,"lineAttrvalName":"","lineAttrvalNameCn":"","picUrl":""}]}],"itemSkuList":[{"inventory":3297,"retailPrice":123.0,"saleStatus":1,"skuCode":"","itemSkuAttrvalList":null,"skuMD5":"d539fdb8079f55eadfc8fa1b6ca8e63e","prodSkuAttrvalList":null}],"itemSpecSelfDefList":[],"itemWholesaleRangeList":[]}'}
    x = dictnn['chck_JSON']
    print x
    intt = 'chck_JSON'
    y = dictnn[intt]
    print y
    
    