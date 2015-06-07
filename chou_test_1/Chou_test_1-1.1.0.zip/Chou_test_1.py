def print_lol(lis, level):
    for item in lis:
        if isinstance(item, list) or \
           isinstance(item, dict) or \
           isinstance(item, tuple):
            print_lol(item, level+1)
        else:
            for num in range(level):
                print('\t', end='')
            print(item)
            
