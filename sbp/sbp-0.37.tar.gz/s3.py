from sbp.client.loggers.json_logger import MultiJSONLogIterator

handles = MultiJSONLogIterator.s3_handles('AKIAIIAAVE4YPHKMDAQQ', 's0M1Vx/GyH3svs8UPjPFPMmnRkJHEsVl7CYTqNve', 'mfine-fluentd', ['devices/789/logs/2015042119', 'devices/789/logs/20150421'])
with MultiJSONLogIterator(handles) as log:
  for delta, timestamp, msg in log.next():
    print msg
