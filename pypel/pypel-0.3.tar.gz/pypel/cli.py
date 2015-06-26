# coding: utf-8
"""pypel.cli, CLI interface for pypel.

THIS SOFTWARE IS UNDER BSD LICENSE.
Copyright (c) 2012-2015 Daniele Tricoli <eriol@mornie.org>

Read LICENSE for more informations.
"""

import argparse
import time
import os
import warnings

from datetime import datetime

try:
    from pygments.console import ansiformat
except ImportError:
    ansiformat = None

from pypel import get_version
try:
    from .gpg import sign, verify
    gnupg = True
except ImportError:
    gnupg = False
from .models import (delete_metadata, set_metadata, make_receipt,
                     DoesNotExist, IsADirectory, ImageNotSupported)

PYPELKEY = os.environ.get('PYPELKEY')


class Row(dict):
    """Representation of a receipt as a row for terminal output."""

    FLOAT_PRECISION = '.2'

    def __init__(self, dct=None):
        if dct is not None:
            self.update(dct)

    def len(self, key=None):
        """Return len of specified field"""
        if key is not None:
            if isinstance(self[key], float):
                fmt = '%%%sf' % Row.FLOAT_PRECISION
                return len(str(fmt % self[key]))

            return len(str(self[key]))

    def format(self, key, align='', precision='', type_=''):
        if isinstance(self[key], float):
            align = '>'
            precision = Row.FLOAT_PRECISION
            type_ = 'f'

        return '{%s:%s{%s}%s%s}' % (key,
                                    align,
                                    key + '_len',
                                    precision,
                                    type_)


class Table(object):

    def __init__(self):
        self.max_len = {}
        self.rows = []

    def add_row(self, row):
        self.rows.append(row)

        if not self.max_len:
            self.max_len.update({column + '_len': 0 for column in row})

        for column in row:
            key_len = column + '_len'
            self.max_len[key_len] = max((row.len(column),
                                         self.max_len[key_len]))

    def to_string(self,
                  color=False,
                  fields_order=None,
                  sep=' -- ',
                  verify=False):

        if fields_order is None:
            fields_order = ['file', 'price', 'retailer', 'note']

        for row in self.rows:

            fmt_str = sep.join([row.format(field) for field in fields_order])

            if verify and not color:
                fmt_str += ' | {}'.format(row['verified'])

            if verify and color:
                if ansiformat:
                    if row['verified']:
                        fmt_str = ansiformat('green', fmt_str)
                    else:
                        fmt_str = ansiformat('red', fmt_str)
                else:
                    warnings.warn('You must install pygments to have colored '
                                  'output.')

            fields = row.copy()
            fields.update(self.max_len)
            yield fmt_str.format(**fields)


def make_parsers():
    """Create the parsers for the CLI tool."""

    parser = argparse.ArgumentParser(description='Easy receipts management.',
                                     version=get_version())
    subparsers = parser.add_subparsers(dest='command_name', help='commands')

    # A show command
    show_parser = subparsers.add_parser('show',
                                        help='Show receipts\' metadata')
    show_parser.add_argument('-v', '--verify', action='store_true',
                             help='verify receipts')
    show_parser.add_argument('-c', '--color', action='store_true',
                             help='colorize the output')
    show_parser.set_defaults(action=do_show)

    # A set command
    set_parser = subparsers.add_parser('set', help='Set receipts\' metadata')
    set_parser.add_argument('-p', '--price', action='store', type=float,
                            help='set receipts\' price')
    set_parser.add_argument('-r', '--retailer', action='store', type=str,
                            help='set receipts\' retailer')
    set_parser.add_argument('-n', '--note', action='store', type=str,
                            help='set receipts\' note')
    set_parser.set_defaults(action=do_set)

    # A delete command
    del_parser = subparsers.add_parser('del',
                                       help='Delete receipts\' metadata')
    del_parser.add_argument('-p', '--price', action='store_true',
                            help='delete receipts\' price')
    del_parser.add_argument('-r', '--retailer', action='store_true',
                            help='delete receipts\' retailer')
    del_parser.add_argument('-n', '--note', action='store_true',
                            help='delete receipts\' note')
    del_parser.set_defaults(action=do_del)

    # A sum command
    sum_parser = subparsers.add_parser('sum', help='Sum receipts\' price')
    sum_parser.set_defaults(action=do_sum)

    # A gpg command
    gpg_parser = subparsers.add_parser('gpg', help='Sign or verify receipts')
    gpg_group = gpg_parser.add_mutually_exclusive_group()
    gpg_group.add_argument('-s', '--sign', action='store_true',
                           help='sign receipts')
    gpg_group.add_argument('-v', '--verify', action='store_true',
                           help='verify receipts')
    gpg_parser.set_defaults(action=do_gpg)

    all_subparsers = dict(
        show_parser=show_parser,
        set_parser=set_parser,
        del_parser=del_parser,
        sum_parser=sum_parser,
        gpg_parser=gpg_parser)

    # HACK: This can be fixed when http://bugs.python.org/issue9540 will be
    # closed.
    for subparser in all_subparsers:
        all_subparsers[subparser].add_argument('receipts',
                                               metavar='receipt',
                                               nargs='+',
                                               help='one or more receipts in a'
                                                    ' supported format')

    return parser, all_subparsers


def receipts(args):
    for receipt_file in args.receipts:

        try:
            receipt = make_receipt(receipt_file)
            yield receipt
        except DoesNotExist as e:
            print('{}: {}'.format(receipt_file, e))
            continue
        except IsADirectory as e:
            print('{}: {}'.format(receipt_file, e))
            continue
        except ImageNotSupported as e:
            # Skip if receipt_file is not a supported file.
            continue


def do_show(args):

    table = Table()

    for receipt in receipts(args):
        row = Row(receipt.asdict())

        # Verify signature for the receipt if needed. If signature is
        # missing `verified' must be False.
        if args.verify:
            if not gnupg:
                warnings.warn('You must install gnupg module to sign and'
                              ' verify receipts.')
            try:
                verified = verify(receipt.file).valid
            except (ValueError, IOError, NameError):
                verified = False

            row.update(dict(verified=verified))

        table.add_row(row)

    print('\n'.join(table.to_string(color=args.color, verify=args.verify)))


def do_set(args):
    for receipt in receipts(args):
        set_metadata(receipt, args.price, args.retailer, args.note)


def do_del(args):
    for receipt in receipts(args):
        delete_metadata(receipt, args.price, args.retailer, args.note)


def do_sum(args):
    price_sum = 0
    for receipt in receipts(args):
        if receipt.price is not None:
            price_sum += receipt.price

    print('{0:.2f}'.format(price_sum))


def do_gpg(args):
    if gnupg:
        for receipt in receipts(args):
            if args.sign:
                sign(receipt.file, keyid=PYPELKEY)

            if args.verify:
                try:
                    verified = verify(receipt.file)
                    if verified:
                        print('Good signature from "{}"'.format(
                              verified.username))
                        d = datetime.fromtimestamp(float(verified.timestamp))
                        print('Signature made {} {} using key ID {}'.format(
                              d.isoformat(' '),
                              time.tzname[time.daylight],
                              verified.key_id))
                except ValueError as err:
                    print('{}: {}'.format(receipt.file, err))
                except IOError as err:
                    print('{}: {}'.format(err.filename, err.strerror))
    else:
        warnings.warn('You must install gnupg module to sign and verify'
                      ' receipts.')


def main():

    parser, subparsers = make_parsers()
    args = parser.parse_args()

    if args.command_name == 'set':
        if args.price is None and args.retailer is None and args.note is None:
            subparsers['set_parser'].error('You must provide at least '
                                           '--price or --retailer or --note')
    elif args.command_name == 'gpg':
        if not args.sign and not args.verify:
            subparsers['gpg_parser'].error('You must provide at least '
                                           '--sign or --verify')
    args.action(args)
