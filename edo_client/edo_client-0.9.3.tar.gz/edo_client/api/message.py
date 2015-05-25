# -*- coding: utf-8 -*-
import hashlib
import json
import time
from .base import BaseApi
from edo_client.error import ApiError


class MessageV2Api(BaseApi):
    def trigger_event(self, channel_type, channel_names, event_name, event_data=None, account=None, instance=None, event_type='transient'):
        if not account: account = self.account_name
        if not instance: instance = self.instance_name
        if channel_type not in ('notify', 'private', 'group', ):
            raise ApiError(400, 400, 'Unexpected value for `channel_type`: %s' % str(channel_type))
        if event_type not in ('persistent', 'transient', ):
            event_type = 'transient'
        try:
            event_data = json.dumps(event_data)
        except Exception, e:
            event_data = '{}'
        try:
            channel_names = json.dumps(channel_names)
        except Exception, e:
            raise ApiError(400, 400, 'Invalid value for `channel_names`: %s' % str(channel_names))
        return self._post('/api/v2/message/trigger_event', 
                          account=account, instance=instance, 
                          event_name=event_name, event_data=event_data, 
                          channel_names=channel_names, channel_type=channel_type, 
                          event_type=event_type)

class MessageApi(BaseApi):
    def __init__(self, *args, **kwargs):
        self.client_id = kwargs.pop('client_id', None)
        super(MessageApi, self).__init__(*args, **kwargs)

    def get_secret(self, account=None, instance=None):
        if not account: account = self.account_name
        if not instance: instance = self.instance_name
        return self._get('/api/v1/admin/get_secret', account=account, instance=instance)

    def refresh_secret(self, account=None, instance=None):
        if not account: account = self.account_name
        if not instance: instance = self.instance_name
        return self._get('/api/v1/admin/refresh_secret', 
                         account=account, instance=instance)

    def connect(self, account=None, instance=None, username=None, timestamp=None, signature=None):
        '''
        Connect to MessageCenter, get personal topic & client id
        '''
        if not account: account = self.account_name
        if not instance: instance = self.instance_name
        client_id = self.client_id or None
        resp = self._post('/api/v1/message/connect', 
                          account=account, instance=instance, 
                          client_id=client_id, username=username, 
                          timestamp=timestamp, signature=signature)
        self.client_id = resp.get('client_id', self.client_id)
        return resp

    def trigger_event(self, user_id, event_name, event_data={}, account=None, instance=None):
        '''
        Trigger event
        '''
        if not account: account = self.account_name
        if not instance: instance = self.instance_name
        event_data = event_data or {}
        return self._post('/api/v1/message/trigger_event', user_id=user_id, 
                          event_name=event_name, event_data=json.dumps(event_data), 
                          account=account, instance=instance)

    def query(self, account=None, instance=None, msg_type=None, channel=None, time_start=None, time_end=None, limit=50):
        '''
        Query history messages
        Args:
            instance: 消息区的实例号
            time_start 起始的消息 ID，默认为第一条未读消息 ID
            time_end 最末一条消息 ID，可选
            limit 消息数量限制，默认 50
        '''
        if not account: account = self.account_name
        if not instance: instance = self.instance_name
        return self._get('/api/v1/message/query', 
                         account=account, 
                         instance=instance, 
                         msg_type=msg_type, 
                         channel=channel, 
                         time_start=time_start, 
                         time_end=time_end, 
                         limit=limit)

    def query_count(self, account=None, instance=None, msg_type=None, channel=None, time_start=None, time_end=None):
        '''
        Query message count within specified time range
        Args:
            instance: 消息区的实例号
            time_start 起始的消息 ID，默认为第一条未读消息 ID
            time_end 最末一条消息 ID，可选
        '''
        if not account: account = self.account_name
        if not instance: instance = self.instance_name
        return self._get('/api/v1/message/query_count', 
                         account=account, 
                         instance=instance, 
                         msg_type=msg_type, 
                         channel=channel, 
                         time_start=time_start, 
                         time_end=time_end)

    def unread_stat(self, account=None, instance=None):
        '''
        Get statics of unread messages
        Args:
            instance: 消息区的实例号
        '''
        if not account: account = self.account_name
        if not instance: instance = self.instance_name
        return self._get('/api/v1/message/unread_stat', 
                         account=account, 
                         instance=instance)

    def join_group(self, group_id, members=[], account=None, instance=None):
        '''
        Add members to given group.
        '''
        if not members: return
        if not account: account = self.account_name
        if not instance: instance = self.instance_name
        return self._post('/api/v1/group/join', 
                          account=account, instance=instance, 
                          group_id=group_id, members=json.dumps(members))

    def leave_group(self, group_id, members=[], account=None, instance=None):
        if not members: return
        if not account: account = self.account_name
        if not instance: instance = self.instance_name
        return self._post('/api/v1/group/leave', 
                          account=account, instance=instance, 
                          group_id=group_id, members=json.dumps(members))

    def update_group(self, group_id, members=[], account=None, instance=None):
        if not members: return
        if not account: account = self.account_name
        if not instance: instance = self.instance_name
        return self._post('/api/v1/group/update', 
                          account=account, instance=instance, 
                          group_id=group_id, members=json.dumps(members))

    def remove_group(self, group_id, account=None, instance=None):
        if not account: account = self.account_name
        if not instance: instance = self.instance_name
        return self._post('/api/v1/group/remove', 
                          account=account, instance=instance, 
                          group_id=group_id)
