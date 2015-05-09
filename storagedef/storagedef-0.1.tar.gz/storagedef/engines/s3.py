# -*- coding: utf-8 -*-

import io
import logging
import mimetypes
from botocore.exceptions import ClientError
from botocore_paste import session_from_config
from paste.deploy.converters import asbool
from zope.interface import implementer
from ..exceptions import DoesNotExist
from ..interfaces import IStorageEngine


logger = logging.getLogger(__name__)


@implementer(IStorageEngine)
class S3StorageEngine(object):

    def __init__(self, **kwargs):
        self.bucket = kwargs.pop('bucket')
        self.region = kwargs.pop('region', None)
        self.acl = kwargs.pop('acl', 'authenticated-read')
        self.protocol_dump = asbool(kwargs.pop('debug', 'false'))
        self.boto_session = session_from_config(kwargs, prefix='')
        self.s3 = self.boto_session.create_client(
            's3',
            region_name=self.region
        )

    def delete(self, filename):
        params = dict(Bucket=self.bucket, Key=filename)
        if self.protocol_dump:
            logger.debug('[PROTO] DeleteObject Call: %r', params)
        ret = self.s3.delete_object(**params)
        if self.protocol_dump:
            logger.debug('[PROTO] DeleteObject Return: %r', ret)

    def exists(self, filename):
        params = dict(Bucket=self.bucket, Key=filename)
        if self.protocol_dump:
            logger.debug('[PROTO] HeadObject Call: %r', params)
        try:
            ret = self.s3.head_object(**params)
        except ClientError as e:
            if self.protocol_dump:
                logger.debug('[PROTO] HeadObject Excepted: %r', e)
            return False

        if self.protocol_dump:
            logger.debug('[PROTO] HeadObject Return: %r', ret)
        return True

    def retrieve(self, filename):
        params = dict(Bucket=self.bucket, Key=filename)
        if self.protocol_dump:
            logger.debug('[PROTO] GetObject Call: %r', params)
        try:
            ret = self.s3.get_object(**params)
        except ClientError as e:
            if self.protocol_dump:
                logger.debug('[PROTO] GetObject Excepted: %r', e)
            if hasattr(e, 'response'):
                if e.response.get('Error', {}).get('Code') == 'NoSuchKey':
                    raise DoesNotExist(filename)
            raise

        if self.protocol_dump:
            logger.debug('[PROTO] GetObject Return: %r', ret)
        return io.BytesIO(ret['Body'].read())  # TODO: cache to tempfile

    def store(self, filename, fileobj):
        params = dict(
            Bucket=self.bucket,
            Key=filename,
            Body=fileobj,
            ACL=self.acl,
            ContentType='application/octet-stream'
        )
        content_type, encoding = mimetypes.guess_type(filename)
        if content_type is not None:
            params['ContentType'] = content_type
        if self.protocol_dump:
            logger.debug('[PROTO] PutObject Call: %r', params)
        ret = self.s3.put_object(**params)
        if self.protocol_dump:
            logger.debug('[PROTO] PutObject Return: %r', ret)
