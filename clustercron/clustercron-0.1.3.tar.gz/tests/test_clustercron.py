"""
Tests for `clustercron` module.
"""

from clustercron import clustercron
import pytest


def test_opt_arg_parser_init():
    opt_arg_parser = clustercron.Optarg([])
    assert opt_arg_parser.arg_list == []
    assert opt_arg_parser.exitcode == 3
    assert opt_arg_parser.args == {
        'version': False,
        'help': False,
        'verbose': False,
        'dry_run': False,
        'lb_type': None,
        'lb_name': None,
        'command': [],
    }


def test_opt_arg_parser_usage():
    opt_arg_parser = clustercron.Optarg([])
    assert opt_arg_parser.usage == '''usage:  clustercron [options] elb <loadbalancer_name> <cron_command>
        clustercron [options] haproxy <loadbalancer_name> <cron_command>

Options:
(-n|--dry-run)   Dry-run, do not run <cron_command>
                 shows where <cron_command> would have ran.
(-v|--verbose)   Verbose output.

        clustercron --version
        clustercron (-h|--help)
'''


@pytest.mark.parametrize('arg_list,args', [
    (
        [],
        {
            'version': False,
            'help': False,
            'verbose': False,
            'dry_run': False,
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
            'dry_run': False,
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
            'dry_run': False,
            'lb_type': None,
            'lb_name': None,
            'command': [],
        }
    ),
    (
        ['-v', '-n', 'elb', 'my_lb_name', 'update', '-r', 'thing'],
        {
            'version': False,
            'help': False,
            'verbose': True,
            'dry_run': True,
            'lb_type': 'elb',
            'lb_name': 'my_lb_name',
            'command': ['update', '-r', 'thing'],
        }
    ),
    (
        ['-n', 'haproxy', 'my_lb_name', 'update', '-r', 'thing'],
        {
            'version': False,
            'verbose': False,
            'help': False,
            'dry_run': True,
            'lb_type': 'haproxy',
            'lb_name': 'my_lb_name',
            'command': ['update', '-r', 'thing'],
        }
    ),
    (
        ['elb', '-n', 'my_lb_name', 'update', '-r', 'thing'],
        {
            'version': False,
            'help': False,
            'verbose': False,
            'dry_run': False,
            'lb_type': 'elb',
            'lb_name': None,
            'command': ['my_lb_name', 'update', '-r', 'thing'],
        }
    ),
    (
        ['haproxy', '-n', 'my_lb_name', 'update', '-r', 'thing'],
        {
            'version': False,
            'help': False,
            'verbose': False,
            'dry_run': False,
            'lb_type': 'haproxy',
            'lb_name': None,
            'command': ['my_lb_name', 'update', '-r', 'thing'],
        }
    ),
    (
        ['-v', 'haproxy', '-n', 'my_lb_name', 'update', '-r', 'thing'],
        {
            'version': False,
            'help': False,
            'verbose': True,
            'dry_run': False,
            'lb_type': 'haproxy',
            'lb_name': None,
            'command': ['my_lb_name', 'update', '-r', 'thing'],
        }
    ),
])
def test_opt_arg_parser(arg_list, args):
        print(arg_list)
        optarg = clustercron.Optarg(arg_list)
        optarg.parse()
        assert optarg.args == args
