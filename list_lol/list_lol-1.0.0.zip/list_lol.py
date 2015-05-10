'list lo'

def print_lol(the_list):
	'this is the print_lol function'
	for li in the_list:
		if isinstance(li, list):
			print "------"
			print_lol(li)
		else:
			print li


