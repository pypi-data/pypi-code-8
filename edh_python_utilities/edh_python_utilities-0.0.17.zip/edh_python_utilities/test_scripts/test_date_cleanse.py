__author__ = 'Eric Meisel'

from edh_python_utilities import cleanse

dateToCleanse = raw_input("Please provide a date for testing: ")

print "Cleansed date strict with defaults: %s"%(cleanse.cleanse_date(dateToCleanse))
print "Cleansed date loose with defaults: %s"%(cleanse.cleanse_date(dateToCleanse, looseCleanse=True))
print "Cleansed date strict with day first: %s"%(cleanse.cleanse_date(dateToCleanse, day_first=True))
print "Cleansed date loose with day first: %s"%(cleanse.cleanse_date(dateToCleanse, looseCleanse=True, day_first=True))
print "Cleansed date strict with year first: %s"%(cleanse.cleanse_date(dateToCleanse, year_first=True))
print "Cleansed date loose with year first: %s"%(cleanse.cleanse_date(dateToCleanse, looseCleanse=True, year_first=True))
print "Cleansed date strict with both first: %s"%(cleanse.cleanse_date(dateToCleanse, year_first=True, day_first=True))
print "Cleansed date loose with both first: %s"%(cleanse.cleanse_date(dateToCleanse, looseCleanse=True, year_first=True, day_first=True))

