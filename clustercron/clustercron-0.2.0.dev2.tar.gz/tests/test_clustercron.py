"""
Tests for `clustercron` module.
"""

from clustercron import clustercron
import pytest


def test_opt_arg_parser_init():
    opt_arg_parser = clustercron.Optarg([])
    assert opt_arg_parser.arg_list == []
    assert opt_arg_parser.args == {
        'version': False,
        'help': False,
        'verbose': False,
        'lb_type': None,
        'lb_name': None,
        'command': [],
    }


def test_opt_arg_parser_usage():
    opt_arg_parser = clustercron.Optarg([])
    assert opt_arg_parser.usage == '''usage:
   clustercron [(-v|--verbose)] elb <loadbalancer_name> [<cron_command>]
   clustercron --version
   clustercron (-h|--help)

Clustercron is cronjob wrapper that tries to ensure that a script gets run
only once, on one host from a pool of nodes of a specified loadbalancer.

Without specifying a <cron_command> clustercron will only check if the node
is the `master` in the cluster and will return 0 if so and return 1 if not.
'''


@pytest.mark.parametrize('arg_list,args', [
    (
        [],
        {
            'version': False,
            'help': False,
            'verbose': False,
            'lb_type': None,
            'lb_name': None,
            'command': [],
        }
    ),
    (
        ['-h'],
        {
            'version': False,
            'help': True,
            'verbose': False,
            'lb_type': None,
            'lb_name': None,
            'command': [],
        }
    ),
    (
        ['--help'],
        {
            'version': False,
            'help': True,
            'verbose': False,
            'lb_type': None,
            'lb_name': None,
            'command': [],
        }
    ),
    (
        ['-v', 'elb', 'my_lb_name', 'update', '-r', 'thing'],
        {
            'version': False,
            'help': False,
            'verbose': True,
            'lb_type': 'elb',
            'lb_name': 'my_lb_name',
            'command': ['update', '-r', 'thing'],
        }
    ),
    (
        ['elb', 'my_lb_name', 'update', '-r', 'thing'],
        {
            'version': False,
            'help': False,
            'verbose': False,
            'lb_type': 'elb',
            'lb_name': 'my_lb_name',
            'command': ['update', '-r', 'thing'],
        }
    ),
    (
        ['elb', 'my_lb_name'],
        {
            'version': False,
            'help': False,
            'verbose': False,
            'lb_type': 'elb',
            'lb_name': 'my_lb_name',
            'command': [],
        }
    ),
    (
        ['elb'],
        {
            'version': False,
            'help': False,
            'verbose': False,
            'lb_type': 'elb',
            'lb_name': None,
            'command': [],
        }
    ),
    (
        ['haproxy', 'my_lb_name', 'update', '-r', 'thing'],
        {
            'version': False,
            'help': False,
            'verbose': False,
            'lb_type': None,
            'lb_name': None,
            'command': [],
        }
    ),
])
def test_opt_arg_parser(arg_list, args):
        print(arg_list)
        optarg = clustercron.Optarg(arg_list)
        optarg.parse()
        assert optarg.args == args
