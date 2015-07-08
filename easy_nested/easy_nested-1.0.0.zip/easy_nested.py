"""
my first comment
"""
def print_lol(my_list):
	# code from Head 1st Python
	for tiap_list in my_list:
		if isinstance(tiap_list, list):
			print_lol(tiap_list)
		else:
			print(tiap_list)