
#这是一个函数
def print_lof(the_list):
#递归
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lof(each_item)
		else:
			print(each_item)


