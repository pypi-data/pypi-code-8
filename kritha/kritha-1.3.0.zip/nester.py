'''该模块实现打印多层嵌套列表元素的功能
1.1.0版本提供嵌套列表缩进功能
1.2.0将缩进量作为可选参数，以向后兼容
1.3.0版本将是否缩进作为可选参数'''

def print_list(list_name,inlen=False,level=0):
    '''函数名为print_list，接收3个参数，其中
    list_name是要打印的列表；
    inlen决定是否缩进；
    level是缩进量'''
    for item in list_name:
        if isinstance(item,list):
            print_list(item,inlen,level+1)#每嵌套一层列表，缩进增加一个制表符
        else:
            if inlen:#inlen为True时才缩进
                for num in range(level):
                    print('\t',end='')
            print(item)
