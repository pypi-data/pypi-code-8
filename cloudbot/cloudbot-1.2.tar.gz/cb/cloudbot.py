"""
Usage:
  cloudbot list <cloud_element> <output_f>
"""
from docopt import docopt
import boto.ec2
import boto.ec2.elb
import boto.rds
import json

AWS_ACCESS_KEY = "AKIAJP7AZ2FSCWEVJ7WA"
AWS_SECRET_KEY = "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"
def docli():
  args = docopt(__doc__)
  return args

def getconn(region="us-west-2", type="ec2"):
  if "ec2" in type:
    conn=boto.ec2.connect_to_region(region, aws_access_key_id=monitoringplatform_user, aws_secret_access_key=monitoringplatform_key)
  if "elb" in type:
    conn=boto.ec2.elb.connect_to_region(region, aws_access_key_id=monitoringplatform_user, aws_secret_access_key=monitoringplatform_key)
  if "rds" in type:
    conn=boto.rds.RDSConnection(aws_access_key_id=monitoringplatform_user, aws_secret_access_key=monitoringplatform_key)
  return conn

def list():
  def wrap_json(element):
    encap_json = {
      "element": element
    }
    return json.dumps(encap_json)
  args = docli()
  if "rds" in args["<cloud_element>"]:
    conn = getconn(type="rds")
    databases = conn.get_all_dbinstances()
    database_structs = []
    for database in databases:
        struct = (database.endpoint, database.id)
        database_structs.append(struct)
    with open(args["<output_f>"], "w") as f:
      f.write(wrap_json(databases))

  if "elb" in args["<cloud_element>"]:
    conn = getconn(type="elb")
    balancers = conn.get_all_load_balancers()
    balancer_structs = []
    for balancer in balancers:
        struct = (balancer.dns_name, balancer.name)
        balancer_structs.append(struct)
    with open(args["<output_f>"], "w") as f:
      f.write(wrap_json(balancer_structs))

def main():
  list()
if __name__ == "__main__":
  main()
