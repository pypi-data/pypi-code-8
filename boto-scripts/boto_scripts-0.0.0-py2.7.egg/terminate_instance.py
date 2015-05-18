#!/usr/bin/env python
import boto.ec2
import os
from optparse import OptionParser
import sys
import yaml


dirname = os.path.abspath(os.path.dirname(__file__))
config = yaml.load(open(os.path.join(dirname,"config.yaml"), "r"))

def getConnection():
  return boto.ec2.connect_to_region(config['REGION'], \
                                    aws_access_key_id = config['AWS_ACCESS_KEY_ID'],
                                    aws_secret_access_key = config['AWS_SECRET_ACCESS_KEY'])



def terminateInstance(instanceId):
  conn = getConnection()
  conn.terminate_instances(instance_ids=[instanceId])

if __name__=='__main__':

  parser = OptionParser()
  parser.add_option('-i', '--instance-id', dest = 'instanceId',
                    type = "string",help = 'The Instance to be terminated')
  (options, args) = parser.parse_args()

  instanceId = options.instanceId

if not instanceId :
  print "Please provide the instance-id to teardown it."
  sys.exit(1)

print "Terminating Instance %s" % instanceId
terminateInstance(instanceId)
