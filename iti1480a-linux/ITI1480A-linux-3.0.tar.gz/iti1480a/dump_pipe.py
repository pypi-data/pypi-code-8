#!/usr/bin/python
from iti1480a.parser import *
import argparse
import errno
import sys

def parseTime(value):
    """
    Parse a string timestamp representation into a tic count.
    """
    if ':' in value:
        minute, second = value.split(':')
        minute = int(minute)
    else:
        minute = 0
        second = value
    if '.' in second:
        second, remainder = second.split('.')
        second = int(second)
    else:
        second = 0
        remainder = value
    for separator in '\'"n':
        remainder = remainder.replace(separator, '')
    return (
            (minute * 60 + seconds) * 1000000000 +
            int(remainder.ljust(9, '0')[:9])
        ) / TIME_INITIAL_MULTIPLIER

def parsePipe(value):
    try:
        address, endpoint, direction = value.split('.')
    except ValueError:
        raise argparse.ArgumentTypeError('Malformed pipe identifier')
    if address:
        try:
            address = int(address)
        except TypeError:
            raise argparse.ArgumentTypeError('Non-numeric device addres')
    else:
        address = None
    try:
        endpoint = int(endpoint)
    except TypeError:
        raise argparse.ArgumentTypeError('Non-numeric endpoint')
    direction = direction.lower()
    if direction not in ('i', 'o'):
        raise argparse.ArgumentTypeError('Invalid pipe direction')
    return PipeMatcher(address, endpoint, direction)

class PipeMatcher(object):
    __slots__ = ('address', 'endpoint', 'direction')
    def __init__(address, endpoint, direction):
        self.address = address
        self.endpoint = endpoint
        self.direction = direction

    def matchEndpoint(self, address, endpoint, direction):
        if endpoint != self.endpoint or direction != self.direction:
            return False
        if address and self.address == None:
            self.address = address
        return address == self.address

class DummyHub(object):
    def __init__(self, address):
        pass

    def push(self, tic, transaction_type, data):
        pass

class Pipe(object):
    __slots__ = ('out')
    def __init__(self, out):
        self.out = out

    def push(self, tic, transaction_type, data):
        pass

CHUNK_SIZE = 16 * 1024
def main():
    parser = argparse.ArgumentParser(
        description='Extract a specific data stream from a capture.',
    )
#    parser.add_argument(
#        '-l', '--list', action='store_true',
#        help='List available data streams (disable data dump).',
#    )
    parser.add_argument(
        '-f', '--from', type=parseTime, default=0,
        help='Capture timestamp to start dumping at (included). '
            'Example: "001:13.705\'962\\"900n". Sub-millisecond separators, '
            'minute leading zeros and second trailing zeros are optional, '
            'so an equivalent representation would be "1:13.705962".',
    )
    parser.add_argument(
        '-t', '--to', type=parseTime, default=float('inf'),
        help='Capture timestamp to stop dumping at (excluded).',
    )
    parser.add_argument(
        '-i', '--infile', default=sys.stdin, type=argparse.FileType('r'),
        help='Data source (default: stdin)',
    )
    parser.add_argument(
        '-o', '--outfile', default=sys.stdout, type=argparse.FileType('w'),
        help='Data destination (default: stdout)',
    )
    parser.add_argument(
        'pipe', type=parsePipe, nargs=1,
        help='Device address, endpoint and direction of trafic to dump. '
            'Examples: "14.2.o" dumps outgoing traffic (host-to-device) for '
            'endpoint 2 of device at address 14. "14.2.i" dumps incomming '
            '(device-to-host) traffic for the same endpoint and device. '
            'An empty device address matches the first non-zero address '
            'transfering data for given endpoint and direction, in considered '
            'capture time span.',
    )
    args = parser.parse_args()
    infile = options.infile
    write = options.outfile
    discard = lambda x: None
    def newPipe(address, endpoint):
        raise NotImplementedError
    stream = ReorderedStream(
        Packetiser(
            TransactionAggregator(
                PipeAggregator(
                    discard,
                    discard,
                    DummyHub,
                    newPipe,
                ),
                discard,
            ),
            discard,
        )
    )
    push = stream.push
    read = infile.read
    try:
        while True:
            data = read(CHUNK_SIZE)
            if not data:
                break
            try:
                push(data)
            except ParsingDone:
                break
        stream.stop()
    except IOError, exc:
        # Happens when output is piped to a pager, and pager exits before stdin
        # is fully parsed.
        if exc.errno != errno.EPIPE:
            raise
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()

