from characteristic import Attribute, attributes
from twisted.internet.protocol import ServerFactory
from twisted.logger import Logger, LogPublisher
from twisted.protocols.basic import LineReceiver
import treq


@attributes(
    [
        Attribute(name="factory"),
        Attribute(name="delimiter"),
        Attribute(name="_log"),
        Attribute(name="_get"),
    ]
)
class HTTPRelayer(LineReceiver, object):
    def lineReceived(self, line):
        try:
            deferred = self._get(line)
        except Exception:
            self._log.failure("Exception while relaying {url}", url=line)
        else:
            deferred.addCallbacks(
                callback=lambda response : self._log.info(
                    "{url} - {response.code}",
                    url=line,
                    response=response,
                ),
                errback=lambda failure : self._log.error(
                    "Failed to retrieve {url!r}",
                    url=line,
                    failure=failure,
                ),
            )


@attributes(
    [
        Attribute(name="_delimiter", default_value="\r\n"),
        Attribute(name="_get", default_value=treq.get),
    ],
)
class HTTPRelayerFactory(ServerFactory, object):
    def __init__(self):
        self._publisher = LogPublisher()
        self._log = Logger(observer=self._publisher)

    def buildProtocol(self, addr):
        return HTTPRelayer(
            factory=self,
            delimiter=self._delimiter,
            log=self._log,
            get=self._get,
        )

    def notify(self, observer):
        """
        Publish relayed URLs to the given observer.

        Allows for external things to ask to be notified as URLs are relayed.

        :type observer: ILogObserver

        """

        self._publisher.addObserver(observer)
