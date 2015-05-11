import subprocess
import json
import time
import os
import random
import string
import re

from Instance import Instance
from SecurityGroup import SecurityGroup

def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(l, key = alphanum_key)

BLUEPRINTS_DIRECTORY = '~/.constructor'

def run(*args):
    data = subprocess.check_output(args)

    if len(data) == 0:
        return None

    return json.loads(data)

class Infrastructure(object):

    def __init__(self, environment = 'dev'):
        self.profile = environment
        self.keyname = environment

    def create_instance(self, id, instancetype = 't2.micro', group=None):
        PEM_FILE = os.path.expanduser(BLUEPRINTS_DIRECTORY + '/' + self.keyname + '.pem')

        disks = [{
            "DeviceName": "/dev/sda1",
            "Ebs": {
                "DeleteOnTermination": True,
                "VolumeSize": 50,
                "VolumeType": "gp2"
            }
        }]

        instance_info = run(
            'aws', 'ec2', 'run-instances',
            '--image-id', 'ami-f0b11187',
            '--instance-type', instancetype,
            '--block-device-mappings', json.dumps(disks),
            '--security-groups', 'web-server',
            '--key-name', self.keyname,
            '--profile', self.profile
        )

        instance_id = instance_info['Instances'][0]['InstanceId']

        self.aws('ec2', 'create-tags', '--resources', instance_id, '--tags', 'Key=Name,Value=' + id)

        running = False

        while running == False:
            time.sleep(5)
            state = run('aws', 'ec2', 'describe-instance-status', '--instance-id', instance_id, '--profile', self.profile)

            if len(state['InstanceStatuses']) > 0:
                running = state['InstanceStatuses'][0]['InstanceState']['Code'] == 16

        instance_data = run('aws', 'ec2', 'describe-instances', '--instance-ids', instance_id, '--profile', self.profile)

        instance_dns = instance_data['Reservations'][0]['Instances'][0]['PublicDnsName']

        reachable = False

        while not reachable:
            try:
                subprocess.check_output(['ssh', '-i', PEM_FILE, '-o', 'StrictHostKeyChecking no', 'ubuntu@' + instance_dns, 'whoami'])
                reachable = True
            except subprocess.CalledProcessError:
                time.sleep(5)
                reachable = False

        instance = Instance(infrastructure = self, id = instance_id, instance_dns = instance_dns, pem_file = PEM_FILE)

        if group is not None:
            instance.add_security_group(group)

        return instance

    def create_s3_bucket(self, id):
        oid = id
        counter = 0
        while True:
            try:
                subprocess.check_output(['aws', 's3', 'mb', 's3://' + id, '--profile', self.profile])
                break
            except subprocess.CalledProcessError:
                counter += 1
                id = oid + '-' + str(counter)

        return {
            'id': id
        }

    def get_instance_info(self, id):
        return self.aws('ec2', 'describe-instance-status', '--instance-id', id)

    def create_database(self, id, username, group):
        password = self.generate_random_string(8)

        dbids = [item["DBInstanceIdentifier"] for item in self.list_databases()]

        id = self.get_unique_id_with_counter(id, dbids)

        run(
            'aws', 'rds', 'create-db-instance',
            '--db-instance-identifier', id,
            '--allocated-storage', '20',
            '--db-instance-class', 'db.t1.micro',
            '--engine', 'MySQL',
            '--storage-type', 'gp2',
            '--master-username', username,
            '--master-user-password', password,
            '--vpc-security-group-ids', group.id,
            '--profile', self.profile
        )

        while True:
            db_info = self.get_database_info(id)

            if 'Endpoint' in db_info:
                break;

            time.sleep(5)

        db = {
            'id': id,
            'username': username,
            'password': password,
            'host': db_info['Endpoint']['Address'],
            'port': db_info['Endpoint']['Port'],
            'info': db_info
        }

        group.allow_inbound_port_for_group(db['port']);

        return db

    def create_redis_server(self, id, group):
        ids = [item["CacheClusterId"] for item in self.list_cache_clusters()]

        id = self.get_unique_id_with_counter(id, ids)

        run(
            'aws', 'elasticache', 'create-cache-cluster',
            '--cache-cluster-id', id,
            '--security-group-ids', group.id,
            '--engine', 'redis',
            '--cache-node-type', 'cache.t2.micro',
            '--num-cache-nodes', '1',
            '--profile', self.profile
        )

        while True:
            info = self.get_redis_cluster_info(id)

            if 'CacheNodes' in info:
                break;

            time.sleep(5)

        redis = {
            'id': id,
            'info': info,
            'host': info['CacheNodes'][0]['Endpoint']['Address'],
            'port': info['CacheNodes'][0]['Endpoint']['Port']
        }

        group.allow_inbound_port_for_group(redis['port']);

        return redis

    def get_unique_id_with_counter(self, id, ids):
        if id in ids:
            idmatches = natural_sort([item for item in ids if re.match(id + '-' + '\d+', item) is not None])

            counter = '1'

            if len(idmatches) > 0:
                lastmatch = idmatches[-1]
                counter = str(int(lastmatch.split('-')[-1]) + 1)

            id = id + '-' + counter

        return id

    def create_security_group(self, id):
        ids = [item["GroupName"] for item in self.list_security_groups()]

        id = self.get_unique_id_with_counter(id, ids)

        create_info = run(
            'aws', 'ec2', 'create-security-group',
            '--group-name', id,
            '--description', id,
            '--profile', self.profile
        )

        return SecurityGroup(self, create_info['GroupId'])

    def get_security_group_info(self, id):
        return run(
            'aws', 'ec2', 'describe-security-groups',
            '--group-names', id,
            '--profile', self.profile
        )['SecurityGroups']

    def list_security_groups(self):
        return run(
            'aws', 'ec2', 'describe-security-groups',
            '--profile', self.profile
        )['SecurityGroups']

    def get_redis_cluster_info(self, id):
        return run(
            'aws', 'elasticache', 'describe-cache-clusters',
            '--cache-cluster-id', id,
            '--show-cache-node-info',
            '--profile', self.profile
        )['CacheClusters'][0]

    def list_cache_clusters(self):
        return run(
            'aws', 'elasticache', 'describe-cache-clusters',
            '--profile', self.profile
        )['CacheClusters']

    def get_database_info(self, id):
        return run(
            'aws', 'rds', 'describe-db-instances',
            '--db-instance-identifier', id,
            '--profile', self.profile
        )['DBInstances'][0]

    def list_databases(self):
        return run(
            'aws', 'rds', 'describe-db-instances',
            '--profile', self.profile
        )['DBInstances']

    def aws(self, *args):
        args = list(args)
        args.insert(0, 'aws')
        args.append('--profile')
        args.append(self.profile)
        return run(*args)

    def generate_random_string(self, n):
        return ''.join(random.SystemRandom().choice(string.uppercase + string.digits) for _ in xrange(n))