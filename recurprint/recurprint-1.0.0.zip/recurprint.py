def recurPrintList(L):
    for item in L:
        if isinstance(item,list):
            recurPrintList(item)
        else:
            print item
