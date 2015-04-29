__author__ = 'heven'
from ucloudclient.utils import base


class UdiskManager(base.Manager):
    '''
    disk manager class
    '''

    def get(self, region, udiskid):
        '''

        :param region:
        :param udiskid:
        :return:
        '''

        body = {}
        body['Region'] = region
        body['Action'] = 'DescribeUDisk'
        body['UDiskId.0'] = udiskid

        return self._get(body)

    def list(self, region, offset=None, limin=None, projectid=None):

        body = {}
        body['Region'] = region
        body['Action'] = 'DescribeUDisk'
        if offset:
            body['Offset'] = offset
        if limin:
            body['Limit'] = limin
        if projectid:
            body['ProjectId'] = projectid

        return self._get(body)
