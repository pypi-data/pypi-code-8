# -*- coding: utf-8 -*-
import argparse

import clowder
import isodate


def send_clowder(api_key, status, service_name, value, frequency):
    """Execute the send clowder command."""
    clowder.api_key = api_key

    data = {'name': service_name}

    if value:
        data['value'] = value

    if frequency:
        data['frequency'] = isodate.parse_duration(frequency)

    print('Sending {} - {} - {}'.format(service_name, status, value))

    if status.lower() in ['ok']:
        clowder.ok(data)
    else:
        clowder.fail(data)


def send_clowder_main():
    parser = argparse.ArgumentParser(
        description='Send status checks to clowder.io'
    )
    parser.add_argument(
        'api_key', help='The API key to use when sending the status'
    )
    parser.add_argument(
        'status', choices=['ok', 'fail'], help='The service status to send'
    )
    parser.add_argument(
        'service_name', help='The name of the service'
    )
    parser.add_argument(
        '-v', '--value', help='The value to be sent along'
    )
    parser.add_argument(
        '-f', '--frequency', help='The frequency of checks as ISO8601 duration'
    )
    args = parser.parse_args()
    send_clowder(
        args.api_key, args.status, args.service_name,
        args.value, args.frequency
    )


if __name__ == '__main__':
    send_clowder_main()
