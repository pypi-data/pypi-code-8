"""Code to iterate through nested lists"""

"""Takes the list as input and recursively checks if it contains
nested list and prints its elements to console"""

def processList(inputList,level=0):
	for each_item in inputList:
		if isinstance(each_item,list):
			processList(each_item)
		else:
                        print(each_item)
