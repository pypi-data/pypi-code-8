#mylist=[[2,5,3,8,4,2,6,2],1,7,[2,5,7,8,[5,4,2,5,7,2,4,2,6,7,2],3,2,6,4,3],3,2,8,2,5,3,8,1,4]
"""This is the "itemsRmv.py" module, and it provides one function called itemsRmvDeep
which removes the list of items from nested lists."""
def itemRemove(target, aList):
    for t in target:
        for l in aList:
            if l == t:
                aList.remove(l)

""" This function takes two arguments called "target", which is none nested list, and "aList"
which is any python list(of, possibly, nested lists). Each data item in the "aList"
will be deleted accouting in the provided target list"""
def itemsRmvDeep(target, aList):
    for i in aList:
        if isinstance(i, list):
            itemsRmvDeep(target, i)
        else:
            itemRemove(target, aList)

#itemRmvDeep([3,5,8,4,2], mylist)
#print(mylist)
        
            
