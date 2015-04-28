"""This is the "nestlist.py" module, and it provides one function
called printLol which prints lists that may or may not include nested list."""

def printLol(theList, indent=False, level=0):
    """This function takes a positional argument called "theList", which is any
    Python list (of, possibly, nested list). Each data item in the provided list
    is (recursively) printed to the screen on its own line."""
    for eachItem in theList:
        if isinstance(eachItem, list):
            printLol(eachItem, indent, level+1)

        else:
            if indent:
                for tabStop in range(level):
                    print("\t", end='')
            print(eachItem)
