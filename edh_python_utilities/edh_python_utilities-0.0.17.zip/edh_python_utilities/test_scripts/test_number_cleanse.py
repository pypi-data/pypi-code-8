__author__ = 'Eric Meisel'

from edh_python_utilities import cleanse

numberToCleanse = raw_input("Please provide a number for testing: ")

print "Cleansed number: %s"%(cleanse.cleanse_number(numberToCleanse))
