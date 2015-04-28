__author__ = 'hyphen'
from ucloudclient.utils import base


class UdiskManager(base.Manager):
    '''
    disk manager class
    '''

    def get(self, region, udiskid, offset=None, limit=None,
            projectid=None):
        '''
        :param region:
        :param udiskid:
        :param offset:
        :param limit:
        :param projectid:
        :return:
        '''
        body = {}
        body['Region'] = region
        body['Action'] = 'DescribeUDisk'
        body['UDiskId'] = udiskid
        if offset:
            body['Offset'] = offset
        if limit:
            body['Limit'] = limit
        if projectid:
            body['ProjectId'] = projectid

        return self._get(body)


    def list(self, region, offset=None, limit=None,
             projectid=None):
        '''
        :param region:
        :param offset:
        :param limit:
        :param projectid:
        :return:
        '''
        body = {}
        body['Region'] = region
        body['Action'] = 'DescribeUDisk'
        if offset:
            body['Offset'] = offset
        if limit:
            body['Limit'] = limit
        if projectid:
            body['ProjectId'] = projectid

        return self._get(body)
