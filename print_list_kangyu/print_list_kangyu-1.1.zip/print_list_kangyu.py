#此模块打印传递进来的列表，其中如果含有嵌套列表，则递归打印
def print_list(the_list, level):
	for each in the_list:
		if isinstance(each, list):
			print_list(each, level + 1)
		else:
			for tab in range(level):
				print('\t', end = '')
			print(each)
