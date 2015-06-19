from boto.s3.connection import S3Connection
import boto
from sparweltbitool.config import config
from sparweltbitool.logger import Logger

class S3Client():
    """
    Operations with s3 bucket.
    Check documentation: http://boto.readthedocs.org/en/latest/ref/s3.html
    """

    def __init__(self):
        self.conn = S3Connection(config.get('aws', 'access_key_id'), config.get('aws', 'secret_access_key'))
        self.logger = Logger()

    def send_file_local(self, key, file_path_local):
        """ Fetch all  files for current user."""
        conn = self.conn

        message = "Sending local file: '{}' under a key: '{}' on s3 bucket: '{}' set on region: '{}'".format(
            file_path_local,
            key,
            config.get('aws', 'bucket'),
            config.get('aws', 'region'))

        Logger().debug(message)

        bucket = conn.get_bucket(config.get('aws', 'bucket'))
        if not bucket.get_location():
            conn = boto.s3.connect_to_region(config.get('aws', 'region'))
            bucket = conn.get_bucket(config.get('aws', 'bucket'))

        return bucket.new_key(key).set_contents_from_filename(file_path_local)
