





"""
#version：1.0
#author：Firsword
#date：2015-4-19 16:11:27

一个函数： #print_nest_list#
可以打印嵌套（也可是非嵌套）列表中每个元素，每个元素占一行
"""


def print_nest_list(listname,tabs):
	"""取列表中的某一项，如果其类型为列表，调用函数自身，如果不是列表，直接打印
	tabs--指定第一层缩进几个tab符，以后每层增加一个tab符"""
	for listname in listname:
		if isinstance(listname,list):
			print_nest_list(listname,tabs+1)
		else:
			for num in range(tabs):
				print("\t",end='')
			print(listname)






