# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import re
import pickle
import sys
import os
import datetime

        
#----------------------------------------- global 
""" 이 모듈은 자료처리 관련 많이 사용하는 것들을 모은 것입니다. """
class yunlib:
    def __init__(self):
        pass

    def help(self):
        """
#
#Description: 웹페이지 정보수집용 공통모듈
#version: v1.3
#history: 20150318  최초작성

        """
        print ""


    def load_pickle(self, mypicklefile):
        """ picklefile 의 내용을 읽어서 리턴함
        """
        mylist = []
        with open(mypicklefile, "rb") as fp:
            mylist = pickle.load(fp)
        return mylist



#-----------------------------
    def mydir(self, dir1, *srch):
        """ dir1 에  입력받은 문자열이 있는 function 과 설명을 화면에 표시함
        """
        result=[]
        if len(srch) == 0 :
            result = [d for d in dir1]
        else:
            for s1 in srch:
                for d1 in dir1:
                    myname = d1
                    #mydesc = eval( d1 + ".__doc__")
                    mytarget = myname
                    #if mydesc :
                    #    mytarget += mydesc
                    if s1 in mytarget:
                        result.append(d1)
        s1 = set(result)
        result = list(s1)
        print "find %d results" % len(result)
        for d1 in result:
            print"====================================\n"
            print d1
            try:
                print eval( d1 + ".__doc__")
            except Exception as ex1:
                print ex1

    def strip_text(self, in_str):
        """--입력받은 문자열내에 한글 영문 숫자가 아닌 모든 문자를 없애는 함수"""
        try:
            new_str = re.sub(u"([\u318d\u00B7\u2024\uFF65\u2027\u2219\u30FB]|[^0-9가-힣a-zA-Z]|middot)","", in_str)
            return new_str
        except Exception as exStripText:
            return in_str

    def strip_list(self, list1, idx = 0):
        """--- list1 의  idx 위치값을 strip 한다. """
        for ipos in range(0, len(list1)):
            list1[ipos][idx] = self.strip_text(list1[ipos][idx])
        return list1 


    def get_soup_from_url(self, url):
        """ url 의 html 을 읽어서 utf-8 로 변환하여 soup 객체로 리턴함"""
        try:
            page = urllib2.urlopen(url)
            soup_result = BeautifulSoup(page, from_encoding="utf-8")
            page.close()
            return soup_result
        except Exception as ex128:
            if page:
                page.close()
            return "ERR:%s"%(ex128)

