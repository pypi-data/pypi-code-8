'''
Created on Jun 8, 2015

@author: andrei
'''

import os
import ConfigParser

from boto.s3.connection import S3Connection, OrdinaryCallingFormat
from boto.s3.key import Key

from hgsTools.auxiliary import read_option, str2bool

#reading the global config file
path = os.path.join(os.environ['HOME'], '.hgsconf/hgs_new.cfg')
config = ConfigParser.RawConfigParser()
config.read(path)

AWS_STORAGE_BUCKET_NAME = read_option(config, 'default', 'aws_storage_bucket_name')
AWS_ACCESS_KEY_ID = read_option(config, 'web_interface', 'aws_access_key')
AWS_SECRET_ACCESS_KEY = read_option(config, 'web_interface', 'aws_secret_key')
AWS_S3_HOST = read_option(config, 'web_interface', 'aws_s3_host')
AWS_S3_PORT = int(read_option(config, 'web_interface', 'aws_s3_port'))
AWS_S3_USE_SSL = str2bool(read_option(config, 'web_interface', 'aws_s3_use_ssl'))
AWS_STORAGE_BUCKET_NAME = read_option(config, 'default', 'aws_storage_bucket_name')


def get_connection():
    conn = S3Connection(
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                    host=AWS_S3_HOST,
                    port=AWS_S3_PORT,
                    is_secure=AWS_S3_USE_SSL,
                    calling_format=OrdinaryCallingFormat()
                    )
    return conn 

def upload_file(local_file, remote_path):
    conn = get_connection()
    bucket = conn.get_bucket(AWS_STORAGE_BUCKET_NAME)
    
    k = Key(bucket)
    k.key = os.path.join(remote_path, os.path.basename(local_file))

    k.set_contents_from_filename(local_file)
    
def download_file(remote_file, local_path):
    conn = get_connection()
    bucket = conn.get_bucket(AWS_STORAGE_BUCKET_NAME)
    
    k = Key(bucket)
    k.key = remote_file
    
    k.get_contents_to_filename(os.path.join(local_path, os.path.basename(remote_file)))