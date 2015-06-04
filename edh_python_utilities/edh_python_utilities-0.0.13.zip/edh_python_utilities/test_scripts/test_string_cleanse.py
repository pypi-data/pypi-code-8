__author__ = 'Eric Meisel'

from edh_python_utilities import cleanse

stringToCleanse = raw_input("Please provide a string for testing: ")

print "Cleansed String: %s"%(cleanse.cleanse_string(stringToCleanse))
