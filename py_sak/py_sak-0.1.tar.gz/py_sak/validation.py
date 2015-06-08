import os

def is_float(value):
    return _is_type(float, value)

def is_int(value):
    return _is_type(int, value)

def _is_type(convert, value):
    try:
        convert(value)
        return True
    except:
        return False

def is_valid_file(path):
    return os.path.exists(path) and os.path.isfile(path)

def is_valid_dir(path):
    return os.path.exists(path) and os.path.isdir(path)

def is_readable(path):
    return os.access(os.path.abspath(path), os.R_OK)
