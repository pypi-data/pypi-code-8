

def auto_quote(value):
    x = str(value)
    if isinstance(value, str):
        x = "'" + x + "'"
    return x
