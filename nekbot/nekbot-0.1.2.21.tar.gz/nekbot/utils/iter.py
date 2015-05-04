__author__ = 'nekmo'

def append_or_update(original_list, new_list, override=True):
    for i, arg in enumerate(new_list):
        if i < len(original_list) and override:
            original_list[i] = arg
        elif i >= len(original_list):
            original_list.append(arg)
    return original_list