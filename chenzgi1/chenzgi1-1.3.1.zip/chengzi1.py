def parse(movies,flag=False,num=-1):
	if(isinstance(movies,list)):
		for attr in movies:
			parse(attr,flag,num+1)
	else:
		if(flag):
			print("\t"*num,end='')
		print(movies)

