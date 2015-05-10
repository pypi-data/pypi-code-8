#!/usr/bin/env python

from twisted.internet.task import react
from twisted.internet.defer import inlineCallbacks
import txtorcon

from guppy import hpy


@inlineCallbacks
def main(reactor):
    state = yield txtorcon.build_local_tor_connection(reactor)
    for circuit in state.circuits.values():
        first_relay = circuit.path[0]
        print "Circuit {} first hop: {}".format(circuit.id, first_relay.ip)
    print "heap:"
    print hpy().heap()

if __name__ == '__main__':
    react(main)
