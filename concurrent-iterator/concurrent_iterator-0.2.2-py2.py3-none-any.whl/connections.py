# vim: set fileencoding=utf-8
"""Ways to connect IProducers and IConsumers."""
from abc import ABCMeta, abstractmethod
from itertools import cycle

from concurrent_iterator import WillNotConsume


class AbstractConsumerFanOut(object):
    """Abstract base class for the FanOut configuration of a Producer to
    several Consumers.
    """

    __metaclass__ = ABCMeta

    def __init__(self, producer, consumers, delay=0.1):
        self._producer = iter(producer)
        self._consumers = list(consumers)
        self._delay = delay

    @abstractmethod
    def run(self):
        """Runs until the producer is exhausted."""


class RoundRobinConsumerFanOut(AbstractConsumerFanOut):
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
                        timeout = self._delay
                    #else:
                        # Try with the next one.


class SaturateConsumerFanOut(AbstractConsumerFanOut):
    """Implements fanout sending values to each consumer until they refuse to
    accept a value.
    """

    def run(self):
        consumers = cycle(self._consumers)
        consumer = next(consumers)
        for value in self._producer:
            dispatch_attempts = 0
            timeout = 0
            while True:  # Dispatch value.
                try:
                    consumer.send(value, timeout)
                    break  # Value dispatched.
                except WillNotConsume:
                    if dispatch_attempts >= len(self._consumers):
                        dispatch_attempts = 0
                        timeout += self._delay
                    else:
                        dispatch_attempts += 1
                    consumer = next(consumers)
