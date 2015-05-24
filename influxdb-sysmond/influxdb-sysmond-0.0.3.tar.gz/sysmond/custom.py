# This file is to be used for adding your own custom collectors.
#
# All that you need to do is have a class that extends CollectorThread,
# and have a run() method that returns a dict to be sent to InfluxDB.
#
# class ExampleCollector(CollectorThread):
#   def run(self):
#       import rand
#
#       return [{
#           "name": "your.point",
#           "columns": [
#               "walk"
#           ],
#           "points": [
#               rand.randint(0, 100)
#           ]
#       }]
