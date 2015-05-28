def parse(movies,num=-1):
	if(isinstance(movies,list)):
		for attr in movies:
			parse(attr,num+1)
	else:
		for i in range(num):
			print("\t",end='')
		print(movies)

