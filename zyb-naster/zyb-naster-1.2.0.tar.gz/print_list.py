"""此模块用来输出嵌套列表，共三个参数，第一个是列表，第二个是是否缩进，第三个是缩进多少个制表符，其中后两个参数是可选的"""
def print_list(aList,is_sj=False,level=0):
    """遇到普通的元素就打印，遇到列表元素就递归调用"""
    for oneElement in aList:
        if isinstance(oneElement,list):
            print_list(oneElement,is_sj,level+1)#递归
        else:
            if is_sj:
                for number in range(level):
                    print("\t",end='')
            print(oneElement)
