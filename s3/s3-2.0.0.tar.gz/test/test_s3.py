import logging
import os
import random
import s3
import subprocess
import yaml

PROGNAME = 'test_s3'
LOG_FILEMODE = 'a'
LOG_FILENAME = '%s.log' % PROGNAME
LOG_FORMAT = '%(asctime)s %(levelname)s: %(message)s'
LOG_LEVEL = logging.DEBUG

def create_file(filename, filesize):
    print 'create_file', filename, filesize
    if not os.access(filename, os.F_OK):
        with open(filename, 'w') as fo:
            for i in range(1, filesize + 1):
                fo.write(chr(random.randint(0, 255)))

def delete_files(*filenames):
    print 'delete_file', filenames
    for filename in filenames:
        if os.access(filename, os.F_OK):
            os.remove(filename)
            
def test_file(storage, filename, remote_name, local_name):
    print 'test_file', filename, remote_name, local_name
    headers = {
            'x-amz-meta-physics': "Kant",
            'x-amz-meta-carpal': "tunnel syndrome",
            'x-amz-meta-morphosis': "Kafka",
            }
    exists, metadata = storage.exists(remote_name)
    assert not exists, 'ERROR %s already exists' % remote_name
    storage.write(filename, remote_name, headers=headers)
    print 'uploaded %s to %s' % (filename, remote_name)
    exists, metadata = storage.exists(remote_name)
    assert exists, 'ERROR %s does not exist' % remote_name
    assert metadata == headers, 'ERROR - metadata is not headers\n%s\n%s' % (
            metadata,
            headers)
    headers['x-amz-meta-morphosis'] += ', Franz'
    storage.update_metadata(remote_name, headers=headers)
    metadata = storage.read(remote_name, local_name)
    print 'downloaded %s to %s' % (remote_name, local_name)
    assert metadata == headers, 'ERROR  - metadata is not headers\n%s\n%s' % (
            metadata,
            headers)
    assert os.access(
            local_name, 
            os.F_OK), 'ERROR %s not found' % local_name
    storage.delete(remote_name)
    exists, metadata = storage.exists(remote_name)
    assert not exists, 'ERROR %s exists' % remote_name
    assert 0 == subprocess.call(
            ['diff', filename, local_name]), 'ERROR files are different'
    print 'SUCCESS', filename
        
def main(yaml_filename):       
    logging.basicConfig(
            filemode=LOG_FILEMODE,
            filename=LOG_FILENAME,
            format=LOG_FORMAT, 
            level=LOG_LEVEL)     

    with open(yaml_filename, 'r') as fi:
        config = yaml.load(fi)

    connection = s3.S3Connection(**config['s3'])    
    storage = s3.Storage(connection)

    default_bucket = config['s3']['default_bucket']
    if default_bucket not in [b.name for b in storage.bucket_list()]:
        storage.bucket_create(default_bucket)

    create_file('little', 10000)
    test_file(storage, 'little', 's3_little', 'from_s3_little')
    delete_files('little', 'from_s3_little')

    create_file('big', 123 + s3.S3Facts.multipart_threshhold * 1)
    test_file(storage, 'big', 's3_big', 'from_s3_big')
    delete_files('big', 'from_s3_big')

    storage.bucket_delete(default_bucket)

if __name__ == '__main__':
    import sys

    try:
        if len(sys.argv) != 2:
            raise Exception, 'usage> %s yaml_filename' % sys.argv[0]
        yaml_filename = sys.argv[1]
        main(yaml_filename)
    except Exception, e:
        print e

