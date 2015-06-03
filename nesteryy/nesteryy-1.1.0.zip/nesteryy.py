def prr(thelist):
    """this is a test ldpddfdfsdfdsfs"""
    for each in thelist:
        if isinstance(each, list):
            prr(each)
        else:
            print(each)
