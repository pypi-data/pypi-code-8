def do_print(data, level):
    for item in data: 
        if isinstance(item, list):
            do_print(item,level+1)
        else:
            for step in range(level):
                print("\t", end="")
            print(item)


