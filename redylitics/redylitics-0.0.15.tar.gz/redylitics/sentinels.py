#!/usr/bin/env python
# -*- coding: utf-8 -*-

from redis.sentinel import Sentinel


class SentinelConnection(object):
    """wrapper around a redis sentinel
    """

    def __init__(self, hosts, port=26379, master_name="mymaster"):
        """sets a sentinel connection and stores a master instance name

        :param hosts: a list of ip addresses
        :type hosts: list

        :param port: the port number to connect to the sentinels
        :type port: int

        :param master_name: the name of the master database
        :type master_name: str
        """
        sentinels = [(host, port) for host in hosts]
        self.sentinel = Sentinel(sentinels)
        self.master_name = master_name

    def get_master(self):
        """gets a connection to the master redis instance

        :return: the master instance of the sentinel cluster
        :rtype: redis.StrictRedis
        """
        return self.sentinel.master_for(self.master_name)

    def get_slave(self):
        """gets a connection to one of the slave redis instances

        :return: a slave instance of the sentinel cluster
        :rtype: redis.StrictRedis
        """
        try:
            return self.sentinel.slave_for(self.master_name)
        except:
            return self.get_master()
