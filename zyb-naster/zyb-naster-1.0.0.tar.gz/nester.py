"""此模块用来输出嵌套列表"""
def print_list(aList):
    """此函数递归调用，遇到普通的元素就打印，遇到列表元素就递归调用"""
    for oneElement in aList:
        if isinstance(oneElement,list):
            print_list(oneElement)#递归
        else:
            print(oneElement)