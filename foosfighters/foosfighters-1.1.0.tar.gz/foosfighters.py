"""
"""

def nested_print(data):
    """Formatted print nested list across multiple lines"""
    if isinstance(data, list):
        nested_print(data)
    else:
        print(data)
