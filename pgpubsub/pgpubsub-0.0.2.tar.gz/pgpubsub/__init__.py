import select
import logging
from pprint import pprint

import psycopg2

logger = logging.getLogger(__name__)

NOT_READY = ([], [], [])


class PubSub(object):
    def __init__(self, conn):
        assert conn.autocommit, "Connection must be in autocommit mode."
        self.conn = conn

    def listen(self, channel):
        with self.conn.cursor() as cur:
            cur.execute('LISTEN %s;' % channel)

    def unlisten(self, channel):
        with self.conn.cursor() as cur:
            cur.execute('UNLISTEN %s;' % channel)

    def notify(self, channel, payload):
        with self.conn.cursor() as cur:
            cur.execute('SELECT pg_notify(%s, %s);', (channel, payload))

    def get_event(self):
        self.conn.poll()
        if self.conn.notifies:
            return self.conn.notifies.pop(0)

    def events(self, select_timeout=5, yield_timeouts=False):
        while True:
            if select.select([self.conn], [], [], select_timeout) == NOT_READY:
                if yield_timeouts:
                    yield None
            else:
                self.conn.poll()
                while self.conn.notifies:
                    yield self.conn.notifies.pop(0)


def connect(*args, **kwargs):
    conn = psycopg2.connect(*args, **kwargs)
    conn.autocommit = True
    return PubSub(conn)
