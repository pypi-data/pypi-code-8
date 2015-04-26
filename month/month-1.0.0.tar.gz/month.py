def print_mon(the_list):
#This is print list in list
	for each_month in the_list:
		if isinstance(each_month, list):
			print_mon(each_month)
		else:
			 print(each_month)
