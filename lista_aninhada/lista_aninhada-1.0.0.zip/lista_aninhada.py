__author__ = 'Gugu'

def print_lol(a_list):
    for each_item in a_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)


"""Esta função é relativa à página 40 do livro"""
# Esta função é relativa à página 40 do livro.

