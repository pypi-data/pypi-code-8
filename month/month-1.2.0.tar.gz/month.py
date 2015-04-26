def print_mon(the_list, level=0):
#This is print list in list
#How use : level -> insert 0 : low list tab 
	for each_month in the_list:
		if isinstance(each_month, list):
			print_mon(each_month, level+1)
		else:
			for tabs in range(level):
				print("\t", end='')
			print(each_month)
