'list lo'

def print_lol(the_list, indent=False, level=0):
	'this is the print_lol function'
	for li in the_list:
		if isinstance(li, list):
			print_lol(li, indent, level+1)
		else:
			if indent:
				for tab_stop in range(level):
					print "\t",
			
			print li


