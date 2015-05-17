"""
This is the mahmoq_nestor.py module and it provides one function called print_lol(), which prints lists that may or may not include nested lists
This is from hf_python
"""

def print_lol(the_list, level=0):
  """
  This function takes a positional argument called the_list, which is any python  list. Each data item is the list is (recursively) printed to the screen
  A second arg is used to insert tab-stops
  """
  for each_item in the_list:
    if isinstance(each_item, list):
      print_lol(each_item, level+1)
    else:
      for tab_stop in range(level):
        print("\t", end='')
      print(each_item)

