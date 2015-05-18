#!/usr/bin/env python
import boto
import boto.ec2
import os
from optparse import OptionParser
import sys
import time
import yaml


dirname = os.path.abspath(os.path.dirname(__file__))
config = yaml.load(open(os.path.join(dirname,"config.yaml"), "r"))

def getConnection():
  return boto.ec2.connect_to_region(config['REGION'], \
                                    aws_access_key_id = config['AWS_ACCESS_KEY_ID'],
                                    aws_secret_access_key = config['AWS_SECRET_ACCESS_KEY'])

def launchInstance(ami):

  conn = getConnection()
  image = conn.get_image(ami)

  security_groups = ['basic_server',]

  reservation = image.run(key_name=config['KEY'],
                          security_groups=security_groups,
                          instance_type=config['INSTANCE_TYPE'])

  instance = reservation.instances[0]
  print instance
  instanceId=instance.id
  conn.create_tags([instanceId],
                   {"Name": '%s' % (tag_to_instance or "instance_launched_with_boto")})

  print "Spinning up instance for '%s'. Waiting for it to boot up." % (ami)
  while instance.state == 'pending':
    print "Instance state: %s" % (instance.state)
    time.sleep(10)
    instance.update()

  publicDnsName = instance.public_dns_name
  print "Instance is running, public dns : %s" % publicDnsName
  return publicDnsName,instanceId



if __name__=='__main__':

  parser = OptionParser()
  parser.add_option('-a', '--ami', dest = 'ami', type = "string",
                    help = 'The AMI from which the instance should be launched')
  parser.add_option('-t', '--tag', dest = 'tag', type = "string",
                    help = 'Give a tag to the instance')
  (options, args) = parser.parse_args()

  ami = options.ami
  tag_to_instance = options.tag

if not ami :
  print "Please provide the AMI to bring up the instance."
  sys.exit(1)

#launching instance with the give AMI
publicDnsName, instanceId = launchInstance(ami)
