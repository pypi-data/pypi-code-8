# vim: set fileencoding=utf-8

import logging
import unittest

from concurrent_iterator.connections import RoundRobinFanOut


logging.basicConfig(level=logging.WARNING)


class RoundRobinFanOutTest(unittest.TestCase):

    def test_when_then_producer_is_empty_then_nothing_is_sent_to_the_consumer(self):
        self.skipTest("Not implemented.")

    def test_when_no_consumer_accepts_the_message_then_a_timeout_is_used(self):
        self.skipTest("Not implemented.")

