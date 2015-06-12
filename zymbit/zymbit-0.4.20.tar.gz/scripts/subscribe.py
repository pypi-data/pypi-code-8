#!/usr/bin/env python
import logging
import json
import sys

import dateutil.parser

from zymbit.stream import Stream


class EchoStream(Stream):
    def handle(self, envelope):
        data = json.loads(envelope)

        timestamp = dateutil.parser.parser(data['timestamp'])
        value = data['params'].get('value')

        print('envelope={}, timestamp={}, value={}'.format(
            envelope, timestamp, value))


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    subscriptions = sys.argv[1:]

    if not subscriptions:
        sys.exit('No subscriptions made, exiting')

    EchoStream(subscriptions).run()
