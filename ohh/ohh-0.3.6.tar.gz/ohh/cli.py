import argparse
from ohh import __version__

actions = ['start', 'stop', 'login', 'status', 'setup_shell']


def make_parser():
    parser = argparse.ArgumentParser(description='ohh CLI')
    parser.add_argument('action',
                        metavar='action',
                        type=str,
                        help='the action to execute. available actions: ' + ', '.join(actions),
                        choices=actions)
    parser.add_argument('--basedir',
                        metavar='BASE_DIR',
                        type=str,
                        default='~/.ohh',
                        help='directory containing ohh data')
    parser.add_argument('--version', action='version',
                        version='%(prog)s {version}'.format(version=__version__))
    return parser


def parse():
    parser = make_parser()
    return parser.parse_args()
