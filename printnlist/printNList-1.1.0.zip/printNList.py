"""This is the comment of module"""
def printNList(obj,level=0):
        """this is the content of the function"""
        for item in obj:
                if isinstance(item,list):
                        printNList(item,level+1)
                else:
                        for i in range(level):
                                print("\t",end='')
                        print(item)
                        
movies=["The Holy Grail",1975,"Terry Johnes & Terry Grilliam",91,["Graham Chapan",
        ["Michael Palin","John Cleese","Terry Grilliam","Eric Idle","Terry Johns"]]]
