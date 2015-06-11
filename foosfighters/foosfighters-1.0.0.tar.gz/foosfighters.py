"""
"""

def nested_print(data):
    """
    """
    for item in data:
        if isinstance(item, list):
            for subitem in item:
                if isinstance(subitem, list):
                    for deepest in subitem:
                        print(deepest)
                else:
                    print(subitem)
        else:
            print(item)
