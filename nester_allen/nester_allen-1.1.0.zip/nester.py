__author__ = 'Allen'

def print_test(the_list,level):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_test(each_item,level+1)
        else:
            print(each_item)

movies = ["The Holy Grails", 1975, "Terry Jones & Terry Gilliam", 91, ["Graham Chapman", ["Michiel Palin", "John Cleese", "Terry Gilliam", "Eric idle", "Terry Jones"]]]