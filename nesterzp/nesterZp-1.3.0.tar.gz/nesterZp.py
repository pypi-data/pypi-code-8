from __future__ import print_function

def printLol(the_list,ident = False,Level = 0):
    for eachItem in the_list:
        if isinstance(eachItem,list):
            printLol(eachItem,ident,Level+1)
        else:
            if ident:
                for tab_stop in range(Level):
                    print("\t", end='')
            print (eachItem)

