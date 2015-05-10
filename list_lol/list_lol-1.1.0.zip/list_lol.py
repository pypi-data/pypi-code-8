'list lo'

def print_lol(the_list, level):
	'this is the print_lol function'
	for li in the_list:
		if isinstance(li, list):
			print_lol(li, level+1)
		else:
			for tab_stop in range(level):
				print "\t",
			print li


