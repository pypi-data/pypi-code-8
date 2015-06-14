def print_list_recursively(lists):
    for each_item in lists:
        if isinstance(each_item, list):
            print("\tlist in list")
            print_list_recursively(each_item)
        else:
            print(each_item)
