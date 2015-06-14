def print_list_recursively(lists, tab_indention_num=0):
    for each_item in lists:
        if isinstance(each_item, list):
            print_list_recursively(each_item, tab_indention_num+1)
        else:
            tab_indention_num = int(tab_indention_num)
            if(tab_indention_num < 0):
                tab_indention_num = 0
            for tab_indention in range(tab_indention_num):
                print("\t", end="")
            print(each_item)
