''' 这是scan_list.py模块，提供了一个print_lol()函数，用来打印列表中各个项，其中每个项可能还是列表，所以使用递归 '''
def print_lol(the_list,leve):
	'''这个函数提供了一个位置参数the_list，可以是任何python列表，最终打印这个列表的所有项 
	   leve参数是提供内嵌列表输出制表符的个数，层级显示
	'''
	for val in the_list:
		if isinstance(val,list):
			print_lol(val,leve+1)
		else:
			for i in range(leve):
				print('\t',end='')
			print(val)
