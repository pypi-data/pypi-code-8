def print_all(the_list):
    for item in the_list:
        if isinstance(item,list):
            print_all(item)
        else:
            print(item)
