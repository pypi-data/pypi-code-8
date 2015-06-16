"""
Tests for `clustercron` module.
"""

from __future__ import print_function

import mock
import pytest
from clustercron import elb


def test_Elb_init():
    elb_lb = elb.Elb('mylbname')
    assert elb_lb.lb_name == 'mylbname'


@pytest.mark.parametrize('instance_id,inst_health_states,is_master', [
    (
        u'i-1d564f5c',
        [
            {'instance_id': u'i-1d564f5c', 'state': u'InService'},
            {'instance_id': u'i-cba0ce84', 'state': u'InService'},
        ],
        True,
    ),
    (
        u'i-1d564f5c',
        [
            {'instance_id': u'i-cba0ce84', 'state': u'InService'},
            {'instance_id': u'i-1d564f5c', 'state': u'InService'},
        ],
        True,
    ),
    (
        u'i-1d564f5c',
        [
            {'instance_id': u'i-cba0ce84', 'state': u'Anything'},
            {'instance_id': u'i-1d564f5c', 'state': u'InService'},
        ],
        True,
    ),
    (
        u'i-cba0ce84',
        [
            {'instance_id': u'i-1d564f5c', 'state': u'InService'},
            {'instance_id': u'i-cba0ce84', 'state': u'InService'},
        ],
        False,
    ),
    (
        u'i-cba0ce84',
        [
            {'instance_id': u'i-cba0ce84', 'state': u'InService'},
            {'instance_id': u'i-1d564f5c', 'state': u'InService'},
        ],
        False,
    ),
    (
        u'i-cba0ce84',
        [
            {'instance_id': u'i-cba0ce84', 'state': u'InService'},
            {'instance_id': u'i-1d564f5c', 'state': u'anything'},
        ],
        True,
    ),
    (
        None,
        [
            {'instance_id': u'i-1d564f5c', 'state': u'InService'},
            {'instance_id': u'i-cba0ce84', 'state': u'InService'},
        ],
        False,
    ),
    (
        None,
        [
            {'instance_id': u'i-1d564f5c', 'state': u'InService'},
            {'instance_id': u'i-cba0ce84', 'state': u'InService'},
        ],
        False,
    ),
])
def test_elb_is_master(instance_id, inst_health_states, is_master):
    print(instance_id, inst_health_states, is_master)
    elb_lb = elb.Elb('mylbname')
    assert elb_lb._is_master(
        instance_id, [mock.Mock(**x) for x in inst_health_states]) == is_master
