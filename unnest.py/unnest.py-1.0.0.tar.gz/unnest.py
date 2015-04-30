"""This is the unnest.py module, it provides one function called print_lil()
which prints lists that may or may not include nested lists."""

def print_lil(a_list):
    """This function takes a positional arg called "a_list",
    which is a python list, which may contain nested lists.
    Each list is printed recursively printed to the screen."""
    for each_item in a_list:
        if isinstance(each_item, list):
            print_lil(each_item)
        else:
            print("\t", end='')
            print(each_item)
        
