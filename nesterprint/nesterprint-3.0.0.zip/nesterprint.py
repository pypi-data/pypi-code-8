#-*-coding:utf-8 -*-
__author__ = 'kikita'

# This function is 3.0 version.

def myprint(Mylist,indent=False,level=0):
# level = 0  makes the level parameter an optional one
    for Item in Mylist:
        if isinstance(Item,list):
            # level + 1 makes the hierarchy
            myprint(Item,indent,level+1)
        else:
            # wheter or not use text indent
            if indent:
                # decide whether print indent tab
                for tabs in range(level):
                    print "\t",
                print(Item)
            else:
                print(Item)