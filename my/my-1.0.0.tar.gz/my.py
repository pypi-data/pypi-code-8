def print_aa(_list):
	for each_on in _list:
		if isinstance(each_on,list):
			print_aa(each_on)
		else:
			print(each_on)
