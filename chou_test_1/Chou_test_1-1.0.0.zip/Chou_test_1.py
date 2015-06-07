def print_lol(lis):
    for item in lis:
        if isinstance(item, list) or \
           isinstance(item, dict) or \
           isinstance(item, tuple):
            print_lol(item)
        else:
            print(item)
            
