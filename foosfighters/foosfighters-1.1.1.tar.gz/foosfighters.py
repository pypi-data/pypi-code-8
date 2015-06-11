"""
"""

def nested_print(data, level=0):
    """Formatted print nested list across multiple lines with indentation"""
    for item in data:
        if isinstance(item, list):
            nested_print(item, level + 1)
        else:
            print("\t"*level + item)
