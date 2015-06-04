__author__ = 'Eric Meisel'

from edh_python_utilities import cleanse

dateToCleanse = raw_input("Please provide a date for testing: ")

print "Cleansed date strict with defaults: %s"%(cleanse.cleanse_date(dateToCleanse))
print "Cleansed date loose with defaults: %s"%(cleanse.cleanse_date(dateToCleanse, looseCleanse=True))

