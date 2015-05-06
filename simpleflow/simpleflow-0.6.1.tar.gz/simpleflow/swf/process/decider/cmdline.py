import argparse


__all__ = ['parser', 'parse_args']


def init_parser():
    parser = argparse.ArgumentParser(description='simpleflow decider process')

    parser.add_argument(
        '-l', '--log-level',
        action='store',
        default='INFO',
        help='set log level',
    )

    parser.add_argument(
        '-d', '--domain',
        action='store',
        help='AWS SWF domain',
    )

    parser.add_argument(
        '-w', '--workflow',
        action='store',
        help='path to a workflow object. Example: a.b.c.Workflow',
    )

    parser.add_argument(
        '-N', '--nb-processes',
        action='store',
        default=None,
        help='number of parallel processes that handle decisions',
    )

    return parser


parser = init_parser()
parse_args = parser.parse_args
