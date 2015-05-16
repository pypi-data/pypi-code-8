# -*- coding: utf-8 -*-
import sys
'''这是moviesbz.py模块，提供了一个movies_item函数，这个函数的作用是递归的打印一个列表。其中有可能包含嵌套列表。'''
def movies_item (The_list,indent=False,level=0,filedir=sys.stdout):
    '''这个函数取一个位置参数，名为The_list.The_list可以是任何一个python列表。indent参数可以控制是否打印制表符，默认为不打印列表中的每个数据项会递归的输出到屏幕上，每个数据项各占一行。'''
    for each_item in The_list:
        if isinstance(each_item,list):
            movies_item(each_item,indent,level+1,filedir)
        else:
            if indent:
                for number in range(level):
                    filedir.write ('\t')
            filedir.write(each_item)
            filedir.write('\n')
           


