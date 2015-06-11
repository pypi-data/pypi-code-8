"""
"""

def nested_print(data, indent=False, level=0):
    """Formatted print nested list across multiple lines with optional
    indentation
    
    """
    for item in data:
        if isinstance(item, list):
            nested_print(item, indent, level + 1)
        else:
            print("\t"*level + item if indent else item)
