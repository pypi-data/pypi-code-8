def prr(thelist, indent=False, level=0):
    """this is a test ldpddfdfsdfdsfs"""
    for each in thelist:
        if isinstance(each, list):
            prr(each,indent,level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t",end='')
            print(each)
