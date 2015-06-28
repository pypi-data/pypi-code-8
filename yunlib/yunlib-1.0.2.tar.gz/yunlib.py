#u*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import re
import pickle
import sys
import os
import datetime

        
#----------------------------------------- global 
""" common libarary """
class com:
    def __init__(self):
        pass

    def help(self):
        """
#
#Description: for crawling
#version: v1.3
#history: 20150318  first version

        """
        print ""


    def load_pickle(self, mypicklefile):
        """ After loding the pickle file, return the data
        """
        mylist = []
        with open(mypicklefile, "rb") as fp:
            mylist = pickle.load(fp)
        return mylist



#-----------------------------
    def mydir(self, dir1, *srch):
        """ disoplay the dir() result
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
        """ strip the special characte exception korean unicode character and numeric ascii """
        try:
            new_str = re.sub(u"([\u318d\u00B7\u2024\uFF65\u2027\u2219\u30FB]|[^0-9가-힣a-zA-Z]|middot)","", in_str)
            return new_str
        except Exception as exStripText:
            return in_str

    def strip_list(self, list1, idx = 0):
        """--- list1  idx strip  ex) list[0][3]  list[1][3] """
        for ipos in range(0, len(list1)):
            list1[ipos][idx] = self.strip_text(list1[ipos][idx])
        return list1 


    def get_soup_from_url(self, url):
        """ return utf-8 HTML"""
        try:
            page = urllib2.urlopen(url)
            soup_result = BeautifulSoup(page, from_encoding="utf-8")
            page.close()
            return soup_result
        except Exception as ex128:
            if page:
                page.close()
            return "ERR:%s"%(ex128)

