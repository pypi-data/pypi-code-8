__author__ = 'Eric Meisel'

from edh_python_utilities import cleanse

dateToCleanse = raw_input("Please provide a date for testing: ")

print "Cleansed date strict with defaults: %s"%(cleanse.cleanse_experian_date(dateToCleanse))

