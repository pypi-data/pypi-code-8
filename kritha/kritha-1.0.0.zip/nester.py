movies=['cheng','long',['yang','ye',['li','he']]]
'''该模块实现打印多层嵌套列表元素的功能'''
'''函数名为print_list，接收一个list参数'''
def print_list(list_name):
    for item in list_name:
        if isinstance(item,list):
            print_list(item)
        else:
            print(item)

print_list(movies)
