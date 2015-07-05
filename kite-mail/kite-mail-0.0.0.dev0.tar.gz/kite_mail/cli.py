#!/usr/bin/env python
# -*- coding:utf-8 -*-

import click
from kite.takosan import Tako
from kite_mail.mail  import kiteMail
from kite_mail.utils import help_messages

@click.command(context_settings={'help_option_names' : ['-h', '--help']})
@click.argument('takosan_url', nargs=1, required=True)
@click.option('--channel', 'channels',
        nargs=1, required=True, multiple=True,
        help=help_messages('channel'))
@click.option('--name', nargs=1, default='Mail Notify',
        help=help_messages('name'))
@click.option('--icon', nargs=1, default=':mailbox_with_mail:',
        help=help_messages('icon'))
@click.option('--body/--no-body', default=False,
        help=help_messages('body'))
def main(takosan_url, channels, name, icon, body):

    RAW_MAIL = click.get_text_stream('stdin')
    kite_mail = kiteMail(RAW_MAIL)
    factory = kite_mail.factory

    notify_payload = {
        'name'    : name,
        'icon'    : icon,
        'message' : u':round_pushpin: *{0}*'.format(factory.get_subject()),
        'pretext' : u':black_nib: From: {0[0]} {0[1]}'.format(factory.get_address('from')),
    }

    if body:
        notify_payload['text'] = kite_mail.get_mailpart()

    kite = Tako(takosan_url, channels, notify_payload)
    kite.flying()


if __name__ == '__main__':
    main()
