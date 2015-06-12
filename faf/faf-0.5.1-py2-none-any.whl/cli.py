"""
FAF relays HTTP requests sent over an endpoint to the URLs specified.

Example::

    $ faf tcp:6666

will listen on port 6666 for line-delimited URLs to relay to.

"""

import argparse
import re
import sys

from twisted.internet import reactor
from twisted.internet.endpoints import serverFromString
from twisted.logger import textFileLogObserver

from faf import __version__, datadog
from faf.relayer import HTTPRelayerFactory


parser = argparse.ArgumentParser(
    description="Relay HTTP requests.",
    epilog=re.sub(":\w+:", "", __doc__),  # strip out Sphinx refs
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
parser.add_argument("-V", "--version", action="version", version=__version__)
parser.add_argument(
    "--base-uri",
    help="the base URI to use for lines seen, or by default, always expect "
         "absolute URIs.",
)
parser.add_argument(
    "--lf",
    action="store_true",
    help="use LF (\\n) to delimit URLs instead of the default, CR LF (\\r\\n)",
)
parser.add_argument(
    "--statsd",
    nargs=2,
    help="increment the provided success and error metrics (in that order)"
         "for each relayed event",
)
parser.add_argument(
    "endpoint",
    help="the endpoint to listen on for URLs",
)


def main(reactor=reactor):
    arguments = vars(parser.parse_args())
    endpoint = serverFromString(
        reactor=reactor,
        description=arguments["endpoint"],
    )

    relayer = HTTPRelayerFactory(
        delimiter="\n" if arguments["lf"] else "\r\n",
        base_uri=arguments["base_uri"],
    )
    relayer.notify(textFileLogObserver(sys.stdout))

    statsd = arguments["statsd"]
    if statsd is not None:
        success, error = statsd
        observer = datadog.observer(success_metric=success, error_metric=error)
        relayer.notify(observer)

    endpoint.listen(relayer)
    reactor.run()
