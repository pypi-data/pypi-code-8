#!/usr/bin/env python
# -*- coding: utf-8 -*-

from redis import StrictRedis

from redylitics.sentinels import SentinelConnection


class BaseClient(object):
    """a client interface
    """

    def get_one(self, key):
        """gets the value of a single key

        :param key: the key to retrieve
        :type key: str

        :return: the key's value
        :rtype: int
        """
        raise NotImplementedError

    def get_many(self, keys):
        """gets the values of many keys

        :param keys: a list of keys
        :type keys: list

        :return: a list of key-value tuples
        :rtype: list
        """
        raise NotImplementedError

    def get_one_hash(self, key, subkeys=None):
        """gets a single hash object, optionally filtered to a key

        :param key: the name of the key
        :type key: str

        :param subkeys: a list of hash keys
        :type subkeys: list

        :return: the requested object
        :rtype: dict
        """
        raise NotImplementedError

    def set_one(self, key, value):
        """increments a key by a given value

        :param key: the name to update
        :type key: str

        :param value: the value to increment by
        :type value: int

        :return: the updated value
        :rtype: int
        """
        raise NotImplementedError

    def set_one_hash(self, key, subkey, value):
        """increments a hash key by a given value

        :param key: the name of the hash
        :type key: str

        :param subkey: the name of the hash key to update
        :type subkey: str

        :param value: the value to increment by
        :type value: int

        :return: the updated value
        :rtype: int
        """
        raise NotImplementedError


class SentinelClient(BaseClient):
    """a redis client that holds a sentinel connection and uses master to write and slaves to read
    """

    def __init__(self, sentinel_hosts, sentinel_port=26379, master_name="mymaster"):
        """initializes a sentinel connection

        :param sentinel_hosts: a list of ip addresses
        :type sentinel_hosts: list

        :param sentinel_port: the port number to connect to the sentinels
        :type sentinel_port: int

        :param master_name: the name of the master database
        :type master_name: str
        """
        self.sentinel = SentinelConnection(sentinel_hosts, sentinel_port, master_name)

    def get_one(self, key):
        client = self.sentinel.get_slave()
        return int(client.get(key))

    def get_many(self, keys):
        client = self.sentinel.get_slave()
        keys = sorted(client.keys(keys))
        values = client.mget(keys)
        for index, value in enumerate(values):
            values[index] = int(value)
        return zip(keys, values)

    def get_one_hash(self, key, subkeys=None):
        client = self.sentinel.get_slave()
        if subkeys:
            _res = client.hmget(key, subkeys)
            res = {}
            for index, key in enumerate(subkeys):
                res[key] = int(_res[index])
        else:
            res = client.hgetall(key)
            for key, value in res.items():
                res[key] = int(value)
        return res

    def set_one(self, key, value):
        client = self.sentinel.get_master()
        return client.incrby(key, value)

    def set_one_hash(self, key, subkey, value):
        client = self.sentinel.get_master()
        return client.hincrby(key, subkey, value)


class StrictClient(BaseClient):
    """a wrapper around the redis.StrictRedis object
    """

    def __init__(self, **kwargs):
        """initializes the client object with a `.client` attribute

        :param kwargs: keyword arguments for building a `redis.StrictRedis` client
        :type kwargs: dict
        """
        self.client = StrictRedis(**kwargs)

    def get_one(self, key):
        return self.client.get(key)

    def get_many(self, keys):
        keys = self.client.keys(keys)
        values = self.client.mget(keys)
        return zip(keys, values)

    def get_one_hash(self, key, subkeys=None):
        if subkeys:
            return self.client.hmget(key, subkeys)
        return self.client.hgetall(key)

    def set_one(self, key, value):
        return self.client.incrby(key, value)

    def set_one_hash(self, key, subkey, value):
        return self.client.hincrby(key, subkey, value)
