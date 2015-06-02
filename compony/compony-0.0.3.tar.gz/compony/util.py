import sys

def dictmerge(x, y):
    z = x.copy()
    z.update(y)
    return z

#from http://sourceforge.net/projects/basicproperty/files/basicproperty/0.6.3a/
def flatten(inlist, type=type, ltype=(list,tuple), maxint=sys.maxsize):
    """Flatten out a list."""
    try:
        # for every possible index
        for ind in range(maxint):
            # while that index currently holds a list
            while isinstance(inlist[ind], ltype):
                # expand that list into the index (and subsequent indicies)
                inlist[ind:ind+1] = list(inlist[ind])
            #ind = ind+1
    except IndexError:
        pass
    return inlist

