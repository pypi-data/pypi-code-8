"""
This is the mahmoq_nestor.py module and it provides one function called print_lol(), which prints lists that may or may not include nested lists
This is from hf_python
"""

def print_lol(the_list):
  """
  This function takes a positional argument called the_list, which is any python  list. Each data item is the list is (recursively) printed to the screen
  """
  for each_item in the_list:
    if isinstance(each_item, list):
      print_lol(each_item)
    else:
      print(each_item)

