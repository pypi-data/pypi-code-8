def circle_Print(mList):
	if(isinstance(mList,list)):
		for item in mList:
			if(isinstance(item,list)):
				circle_Print(item)
			else:
				print(item)
	else:
		print(mList)

