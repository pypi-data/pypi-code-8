from unittest import TestCase

from characteristic import Attribute, attributes
from treq.test.test_response import FakeResponse
from twisted.internet import defer
from twisted.logger import formatEvent
from twisted.test.proto_helpers import StringTransport

from faf.relayer import HTTPRelayerFactory


# Sigh, incomplete fakes abound.
class FakeResponse(FakeResponse):
    def __init__(self, request, **kwargs):
        super(FakeResponse, self).__init__(**kwargs)
        self.request = request


@attributes([Attribute(name="absoluteURI")])
class FakeRequest(object):
    pass


def connectedRelayerProtocol(**kwargs):
    factory = HTTPRelayerFactory(get=fakeGet, **kwargs)
    protocol = factory.buildProtocol(("127.0.0.1", 0))
    protocol.makeConnection(StringTransport())
    return protocol


def fakeGet(url):
    request = FakeRequest(absoluteURI=url)
    if url == "http://localhost/succeed":
        response = FakeResponse(code=200, headers=None, request=request)
    elif url == "http://localhost/error":
        response = FakeResponse(code=500, headers=None, request=request)
    else:
        raise Exception("Unknown URL: %r" % (url,))
    return defer.succeed(response)


def assertEventsAre(self, *events):
    """
    Assert that the provided events are the ones that have been logged.

    """

    self.assertEqual(
        [formatEvent(event) for event in self.events], list(events),
    )


class TestRelayer(TestCase):

    assertEventsAre = assertEventsAre

    def setUp(self):
        self.protocol = connectedRelayerProtocol()
        self.events = []
        self.protocol.factory.notify(self.events.append)

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


class TestRelativeRelayer(TestCase):

    assertEventsAre = assertEventsAre

    def setUp(self):
        self.protocol = connectedRelayerProtocol(base_uri="http://localhost")
        self.events = []
        self.protocol.factory.notify(self.events.append)

    def test_successful(self):
        self.protocol.dataReceived("/succeed\r\n")
        self.assertEventsAre("http://localhost/succeed - 200")

    def test_unsuccessful(self):
        self.protocol.dataReceived("/error\r\n")
        self.assertEventsAre("http://localhost/error - 500")

    def test_exception(self):
        self.protocol.dataReceived("/unknown\r\n")
        self.assertEventsAre(u'Exception while relaying /unknown')
