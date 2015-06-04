__author__ = 'Eric Meisel'

from edh_python_utilities import cleanse

dateToCleanse = raw_input("Please provide a date for testing: ")

print "Cleansed date strict: %s"%(cleanse.cleanse_date(dateToCleanse))
print "Cleansed date loose: %s"%(cleanse.cleanse_date(dateToCleanse, True))
