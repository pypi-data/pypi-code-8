#!/usr/bin/env python
# -*- coding:utf-8 -*-

def help_messages(command):

    msg = {
        'channel':
            'Name of notice channel, or id (e.g. #example, @id)',
        'name':
            'set botname',
        'icon':
            'set image url or emoji (e.g. :shachikun:)',
        'body':
            'the flag decide include mail body part. (Default: False) '
    }

    if msg[command] :
        return msg[command]
    else:
        return None
