
"""This is the "neter.py" module and it provides one function called print_lol()
   which prints lists that may not includes nested lists."""

def print_lol(the_list):

    """This function take one positional argument called "the_list" , which is 
       any Python list (of -possibly -nested lists). Each data item in the
       provided list (recursively) printed to the screen on it's own line."""
       
    for each_item in the_list:
        if isinstance(each_item , list):
            print_lol(each_item)       
            
        else:
            print(each_item)    
