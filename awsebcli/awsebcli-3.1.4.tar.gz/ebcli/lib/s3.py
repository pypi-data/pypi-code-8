# Copyright 2014 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

from __future__ import division
import os
from io import BytesIO
import math
import threading
from cement.utils.misc import minimal_logger

from . import aws
from ..objects.exceptions import NotFoundError, FileTooLargeError, UploadError
from ..core import io
from .utils import static_var


LOG = minimal_logger(__name__)
CHUNK_SIZE = 5252880  # Minimum chunk size allowed by S3
THREAD_COUNT = 8  # Number of threads to use for multithreaded mode


def _make_api_call(operation_name, **operation_options):
    return aws.make_api_call('s3', operation_name, **operation_options)


def upload_file(bucket, key, file_path, region=None):
    with open(file_path, 'rb') as fp:
        return _make_api_call('put_object',
                              Bucket=bucket,
                              Key=key,
                              Body=fp,
                              region=region)


def get_object_info(bucket, object_key, region=None):
    result = _make_api_call('list_objects',
                   Bucket=bucket,
                   Prefix=object_key,
                   region=region)

    if 'Contents' not in result or len(result['Contents']) < 1:
        raise NotFoundError('Object not found.')

    objects = result['Contents']
    if len(objects) == 1:
        return objects[0]
    else:
        # There is more than one result, search for correct one
        object_key = next((o for o in objects if o['Key'] == object_key), None)
        if object_key is None:
            raise NotFoundError('Object not found.')
        else:
            return object_key


def get_object(bucket, key, region=None):
    result = _make_api_call('get_object',
                            Bucket=bucket,
                            Key=key,
                            region=region)
    return result['Body'].read()


def upload_application_version(bucket, key, file_path, region=None):
    size = os.path.getsize(file_path)
    LOG.debug('Upload Application Version. File size = ' + str(size))
    if size > 536870912:
        raise FileTooLargeError('Application version cannot be any '
                                'larger than 512MB')
    if size < 7340032:
        result = simple_upload(bucket, key, file_path, region=region)

    else:
        result = multithreaded_upload(bucket, key, file_path, region=region)
    return result


def simple_upload(bucket, key, file_path, region=None):
    io.echo('Uploading', key, 'to S3. This may take a while.')
    result = upload_file(bucket, key, file_path, region=region)
    io.echo('Upload Complete.')
    return result


def multithreaded_upload(bucket, key, file_path, region=None):
    """
    Upload a file in multiple parts using multiple threads.
    Takes advantage of S3's multipart upload.
    :param bucket: S3 bucket name
    :param key: keyname of file to be uploaded
    :param file_path: full path location of file to be uploaded
    :param region: region to use for S3
    :return: Result dictionary
    """

    size = os.path.getsize(file_path)
    total_parts = math.ceil(size / CHUNK_SIZE)  # Number of parts needed
    LOG.debug('Doing multi-threaded upload. Parts Needed=' + str(total_parts))

    # Begin multi-part upload
    upload_id = _get_multipart_upload_id(bucket, key, region)
    io.update_upload_progress(0)

    # Upload parts
    try:
        etaglist = []  # list for part id's (etags)
        with open(file_path, 'rb') as f:
            # Create threads to handle parts of upload
            lock = threading.Lock()
            jobs = []
            for i in range(THREAD_COUNT):
                p = threading.Thread(
                    target=_upload_chunk,
                    args=(f, lock, etaglist, total_parts,
                          bucket, key, upload_id, region),
                    )
                p.daemon = True
                jobs.append(p)
                p.start()

            _wait_for_threads(jobs)

        # S3 requires the etag list to be sorted
        etaglist = sorted(etaglist, key=lambda k: k['PartNumber'])

        # Validate we uploaded all parts
        if len(etaglist) != total_parts:
            LOG.debug('Uploaded {0} parts, but should have uploaded {1} parts.'
                      .format(len(etaglist), total_parts))
            raise UploadError('An error occured while uploading Application Version. '
                              'Use the --debug option for more information if the problem persists.')
        result = _make_api_call('complete_multipart_upload',
                              Bucket=bucket,
                              Key=key,
                              UploadId=upload_id,
                              MultipartUpload=dict(Parts=etaglist))

        return result

    except (Exception, KeyboardInterrupt) as e:
        # We dont want to clean up multipart in case a user decides to
        # continue later
        raise


def _wait_for_threads(jobs):
    alive = True
    while alive:
        alive = False
        for j in jobs:
            """
            We want to wait forever for the thread to finish.
            j.join() however is a halting call. We need to pass in a
            time to j.join() so it is non halting. This way a user can use
            CTRL+C to terminate the command. 2**31 is the largest number we
            can pass into j.join()
            """
            try:
                timeout = threading.TIMEOUT_MAX
            except AttributeError:  # Python 2
                timeout = 2**16  # 18 hours should be sufficient.
            j.join(timeout)
            if j.isAlive():
                alive = True


def _upload_chunk(f, lock, etaglist, total_parts, bucket, key, upload_id,
                  region):
    LOG.debug('Creating child thread')
    while True:
        data, part = _read_next_section_from_file(f, lock)
        if not data:
            LOG.debug('No data left, closing')
            return
        # First check to see if s3 already has part
        for i in range(0, 5):
            try:
                etag = _get_part_etag(bucket, key, part, upload_id, region=region)
                if etag is None:
                    b = BytesIO()
                    b.write(data)
                    b.seek(0)
                    response = _make_api_call('upload_part',
                                              Bucket=bucket,
                                              Key=key,
                                              UploadId=upload_id,
                                              Body=b,
                                              PartNumber=part,
                                              region=region)
                    etag = response['ETag']

                etaglist.append({'PartNumber': part, 'ETag': etag})

                progress = (1/total_parts) * len(etaglist)
                io.update_upload_progress(progress)
                # No errors, break out of loop
                break
            except Exception as e:
                # We want to swallow all exceptions or else they will be
                # printed as a stack trace to the Console
                # Exceptions are typically connections reset and
                # Various things
                LOG.debug('Exception raised: ' + str(e))
                # Loop will cause a retry


def _get_part_etag(bucket, key, part, upload_id, region):
    try:
        response = _make_api_call('list_parts',
                              Bucket=bucket,
                              Key=key,
                              UploadId=upload_id,
                              region=region)
    except Exception as e:
        # We want to swallow all exceptions or else they will be printed
        # as a stack trace to the Console
        LOG.debug('Exception raised: ' + str(e))
        return None

    if 'Parts' not in response:
        return None
    etag = next((i['ETag'] for i in response['Parts']
                 if i['PartNumber'] == part), None)
    return etag


def _get_multipart_upload_id(bucket, key, region):
    # Check to see if multipart already exists
    response = _make_api_call('list_multipart_uploads',
                              Bucket=bucket,
                              Prefix=key,
                              region=region)

    try:
        for r in response['Uploads']:
            if r['Key'] == key:
                return r['UploadId']
    except KeyError:
        pass  # There are no uploads with that prefix

    # Not found, lets initiate the upload
    response = _make_api_call('create_multipart_upload',
                              Bucket=bucket,
                              Key=key,
                              region=region)

    return response['UploadId']


@static_var('part_num', 0)
def _read_next_section_from_file(f, lock):
    try:
        with lock:
            data = f.read(CHUNK_SIZE)
            _read_next_section_from_file.part_num += 1
            return data, _read_next_section_from_file.part_num
    except ValueError as e:
        LOG.debug('Reading file raised error: ' + str(e))
        return '', None  # File was closed, Process was terminated
