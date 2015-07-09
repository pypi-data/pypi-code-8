#-*-coding:utf-8 -*-
__author__ = 'kikita'

# This function is 2.0 version.

def myprint(Mylist,level=0):
# level = 0  makes the level parameter an optional one。
    for Item in Mylist:
        if isinstance(Item,list):
            myprint(Item,level+1)
            #level + 1 makes the hierarchy。
        else:
            for tabs in range(level):
                print "\t",
            print(Item)
