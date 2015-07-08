#在原有功能基础上，增加打印时没出现一层嵌套就缩进显示一个TAB制表符(增加了一个新的参数level(0，1，2))
#为了使模块功能变的更为灵活，把模块中必备的两个参数中的一个改为可选参数为它添加缺省值
def print_list(the_list,level=0):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_list(each_item,level+1) #每打印一次参数+1,表示下次打印列表时多增加一个TAB制表符
        else:
            for tab_stop in range(level):
                  print("\t",end=" ")
            print(each_item)
