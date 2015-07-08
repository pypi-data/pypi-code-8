"""
my first comment
"""
def print_lol(my_list, total_tabs):
	# code from Head 1st Python
	for tiap_list in my_list:
		if isinstance(tiap_list, list):
			print_lol(tiap_list, total_tabs+1)
		else:
                        for num in range(total_tabs):
                                print("\t", end=")        
                        print(tiap_list)
