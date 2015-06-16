# clustercron/elb.py
# vim: ts=4 et sw=4 sts=4 ft=python fenc=UTF-8 ai
# -*- coding: utf-8 -*-

'''
clustercron.elb
---------------
'''

from __future__ import unicode_literals

import logging
import socket
import boto.ec2.elb

from .compat import PY3

if PY3:
    from urllib.request import Request
    from urllib.request import urlopen
    from urllib.error import URLError

else:
    from urllib2 import Request
    from urllib2 import urlopen
    from urllib2 import URLError


logger = logging.getLogger(__name__)


class Elb(object):
    URL_INSTANCE_ID = \
        'http://169.254.169.254/1.0/meta-data/instance-id'

    def __init__(self, lb_name, timeout=3):
        self.lb_name = lb_name
        socket.setdefaulttimeout(timeout)

    def _get_instance_id(self):
        request = Request(self.URL_INSTANCE_ID)
        try:
            response = urlopen(request)
        except URLError:
            instance_id = None
            logger.error('Could not get instance ID')
        else:
            instance_id = response.read()[:10]
            logger.debug('Instance ID: %s', instance_id)
        return instance_id

    def _get_inst_health_states(self):
        try:
            conn = boto.ec2.elb.ELBConnection()
            lb = conn.get_all_load_balancers(
                load_balancer_names=[self.lb_name])[0]
            inst_health_states = lb.get_instance_health()
        except Exception as error:
            logger.error('Could not get instance health states: %s', error)
            inst_health_states = []
        return inst_health_states

    def _is_master(self, instance_id, inst_health_states):
        res = False
        instances_all = sorted([x.instance_id for x in inst_health_states])
        logger.debug('instances: %s', ', '.join(instances_all))
        instances_in_service = sorted([
            x.instance_id for x in inst_health_states
            if x.state == 'InService'
        ])
        logger.debug(
            'Instances in service: %s',
            ', '.join(instances_in_service)
        )
        if instances_in_service:
            res = instance_id == instances_in_service[0]
        return res

    @property
    def master(self):
        instance_id = self._get_instance_id()
        if instance_id:
            inst_health_states = self._get_inst_health_states(self)
            return self._is_master(instance_id, inst_health_states)
        return False
