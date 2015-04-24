"""This Mudoles is used to print the list."""

def print_list(the_list):
	for item in the_list:
		if isinstance(item,list):
			print_list("\t"+item)
		else:
			print(item)

"""This function is used to print all the elements of the list."""

