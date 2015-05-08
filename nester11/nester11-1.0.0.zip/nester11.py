'''这是"nester.py"模块，提供了一个名为llol()的函数，这个函数
的作用是打印列表，其中有可能包含（也可能不包含）嵌套列表。'''
def llol(the_list):
        """这个函数取一个位置参数，名为"the_list",这可以是任何Python
        列表（也可以是包含嵌套列表的列表）。所指定的列表中的每个数据项
        会（递归地）输出到屏幕上，个数据项各占一行。"""
        for each_item in the_list:
                if isinstance(each_item,list):
                        llol(each_item)
                else:
                        print(each_item)



