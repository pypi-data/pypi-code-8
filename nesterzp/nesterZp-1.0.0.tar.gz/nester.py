from __future__ import print_function

def printLol(the_list,Level = 0):
    for eachItem in the_list:
        if isinstance(eachItem,list):
            printLol(eachItem,Level+1)
        else:
            for tab_stop in range(Level):
                print("\t", end='')
            print (eachItem)

