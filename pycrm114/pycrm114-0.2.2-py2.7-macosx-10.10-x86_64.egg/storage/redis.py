import time

from pycrm114.storage import Storage


class RedisStorage(Storage):
    def update_data_block(self, data_block):
        self._client.hset("{}:crm".format(self._namespace), 'last_modified', time.time())
        self._client.hset("{}:crm".format(self._namespace), 'data_block', data_block.dumps())

    def __init__(self, client=None, namespace=None):
        self._client = client
        self._namespace = namespace
        self._lock = None

    @property
    def data_block_string(self):

        return self._client.hget("{}:crm".format(self._namespace), 'data_block')

    @property
    def last_updated(self):
        return self._client.hget("{}:crm".format(self._namespace), "last_modified")

    def acquire_lock(self):
        self._lock = self._client.lock("{}:crm:lock".format(self._namespace))
        self._lock.acquire()

    def release_lock(self):
        if self._lock:
            self._lock.release()
            self._lock = None


