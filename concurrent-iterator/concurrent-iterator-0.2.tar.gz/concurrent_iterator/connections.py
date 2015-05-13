# vim: set fileencoding=utf-8
"""Ways to connect IProducers and IConsumers."""
from abc import ABCMeta, abstractmethod
from itertools import cycle

try:
    from itertools import izip as zip
except ImportError:
    pass  # It's Python 3.


from concurrent_iterator import WillNotConsume


class AbstractFanOut(object):
    """Abstract base class for the FanOut configuration of a Producer to
    several Consumers.
    """

    __metaclass__ = ABCMeta

    def __init__(self, producer, consumers):
        self._producer = iter(producer)
        self._consumers = list(consumers)

    @abstractmethod
    def run(self):
        """Runs until the producer is exhausted."""


class RoundRobinFanOut(AbstractFanOut):
    """Implements fanout sending one value to each consumer round robin."""

    def run(self):
        consumers = cycle(self._consumers)
        for value in self._producer:
            timeout = 0
            for i, consumer in enumerate(consumers):
                try:
                    consumer.send(value, timeout)

                    # Value sent.
                    timeout = 0
                    break
                except WillNotConsume:
                    if i and i % len(self._consumers) == 0:
                        # No consumer accepted this message from now on, wait a
                        # little for each send.
                        timeout = 0.1
                    #else:
                        # Try with the next one.


class SaturateFanOut(AbstractFanOut):
    """Implements fanout sending values to each consumer until they refuse to
    accept a value.
    """

    def run(self):
        # FIXME Add delay for when they are all saturated.
        try:
            value = next(self._producer)
        except StopIteration:
            pass  # The producer is empty.
        else:
            for consumer in cycle(self._consumers):
                try:
                    consumer.send(value)

                    for value in self._producer:
                        consumer.send(value)

                    return  # The producer is exhausted.
                except WillNotConsume:
                    pass  # Lets go for the next consumer.
