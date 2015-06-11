from unittest import TestCase

from treq.test.test_response import FakeResponse
from twisted.internet import defer
from twisted.logger import formatEvent
from twisted.test.proto_helpers import StringTransport

from faf.relayer import HTTPRelayerFactory


def connectedRelayerProtocol():
    factory = HTTPRelayerFactory(get=fakeGet)
    protocol = factory.buildProtocol(("127.0.0.1", 0))
    protocol.makeConnection(StringTransport())
    return protocol


def fakeGet(url):
    if url == "http://localhost/succeed":
        return defer.succeed(FakeResponse(code=200, headers=None))
    elif url == "http://localhost/error":
        return defer.succeed(FakeResponse(code=500, headers=None))
    else:
        raise Exception("Unknown URL: %r" % (url,))


class TestRelayer(TestCase):
    def setUp(self):
        self.protocol = connectedRelayerProtocol()
        self.events = []
        self.protocol.factory.notify(self.events.append)

    def assertEventsAre(self, *events):
        """
        Assert that the provided events are the ones that have been logged.

        """

        self.assertEqual(
            [formatEvent(event) for event in self.events], list(events),
        )

    def test_successful(self):
        self.protocol.dataReceived("http://localhost/succeed\r\n")
        self.assertEventsAre("http://localhost/succeed - 200")

    def test_unsuccessful(self):
        self.protocol.dataReceived("http://localhost/error\r\n")
        self.assertEventsAre("http://localhost/error - 500")

    def test_exception(self):
        self.protocol.dataReceived("http://localhost/unknown\r\n")
        self.assertEventsAre(
            u'Exception while relaying http://localhost/unknown',
        )
