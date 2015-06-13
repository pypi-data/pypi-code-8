# coding: utf-8
"""
Relay
~~~~~

Relay is an irc micro-framework that smells too much like a web framework


Copyright (c) 2015, ldesgoui <relay at ldesgoui dot xyz>
See LICENSE for more informations.
"""

from collections import defaultdict
import logging
import os
import socket

from . import constants
from . import parse


class Relay(object):
    DEFAULT_ROUTE = ":{sender} {command} {args}"
    DEFAULT_CONFIG = dict(user="", port=6667)

    def __init__(self, name):
        self.handlers = defaultdict(set)
        self.client = dict(Relay.DEFAULT_CONFIG)
        self.logger = logging.getLogger(name)
        self.state = defaultdict(dict)

    def __repr__(self):
        classname = self.__class__.__name__
        try:
            client = "{nick}!{user}@{host}:{port}".format(**self.client)
        except KeyError:
            client = "not fully configured"
        routes = len(self.handlers)
        handlers = sum(map(len, self.handlers.values()))
        return "<{} {}, {} routes, {} handlers>".format(
                classname, client, routes, handlers)

    __str__ = __repr__

    def handler(self, arg):
        """ @register decorator """
        def decorator(func, route=arg):
            func.relay_route = route
            self.register(func)
            return func

        if callable(arg):
            """ decorator was not given arguments, it takes DEFAULT_ROUTE """
            return decorator(func=arg, route=Relay.DEFAULT_ROUTE)

        return decorator

    def register(self, func, route=None):
        """
        Used to register a function as a handler
        This function's arguments should match the routes's results
        or at least catch *args and **kwargs.

        This cannot be used with bound methods, as of yet.
        """

        if route is not None and hasattr(func, "relay_route"):
            self.logger.warn("Overriding route for `{}`: from `{}` to `{}`"
                             .format(func, func.relay_route, route))
        if route is None:
            if not hasattr(func, "relay_route"):
                raise AttributeError("Cannot register a handler with no route")
            else:
                route = func.relay_route

        self.logger.debug("Registering handle: `{route}` -> `{func}`"
                          .format(route=route, func=func.__qualname__))
        self.handlers[route].add(func)

    def _from_env(self, values):
        if values is True:
            values = ["host", "port", "user", "nick", "password"]
        if not isinstance(values, dict):
            values = {key: "RELAY_{}".format(key.upper()) for key in values}
        config = dict()
        for key, env_key in values.items():
            val = os.getenv(env_key, None)
            if not val:
                continue
            config[key] = val
        self.config(**config)

    def config(self, **options):
        for key, val in options.items():
            if key == 'from_env':
                self._from_env(val)
                continue
            if key not in ["host", "port", "user", "nick", "password"]:
                continue
            self.client[key] = val
        return self

    def run(self, **options):
        """
        The client in itself

        TODO: make this better, faster, stronger :)
        """
        if 'host' not in self.client or 'nick' not in self.client:
            raise ValueError("Cannot run, missing configuration.")

        self.logger.info("Connecting")
        sock = socket.socket()
        sock.connect((self.client['host'], self.client['port']))
        self.logger.info("Connected")

        def send(message):
            sock.send(("{message}\r\n".format(message=message)).encode())
            self.logger.debug("Send: {message}".format(message=message))

        self.send = send

        send("NICK {nick}".format(**self.client))
        user = self.client.get('user', None) or self.client['nick']
        send("USER {0} {0} {0} :{0}".format(user))
        if 'password' in self.client:
            send("PASS {password}".format(**self.client))

        data = sock.makefile()

        while 42:
            for line in data:
                line = line.strip()
                if not line:
                    continue
                self.logger.debug("Recv: {message}".format(message=line))
                for route, handlers in self.handlers.items():
                    try:
                        args, kwargs = parse.match(route, line)
                    except ValueError:
                        continue
                    for handler in handlers:
                        outs = handler(*args, state=self.state[handler], **kwargs)
                        for out in outs or []:
                            send(out.format(*args, **kwargs))


def _register(route):
    def decorator(func):
        func.relay_route = route
        return func
    return decorator


@_register("PING :{ball}")
def auto_pong(*args, **kwargs):
    """ answer to PING requests """
    yield "PONG :{ball}"


def auto_join(channels):
    @_register(Relay.DEFAULT_ROUTE)
    def auto_join_closure(*args, command=None, arguments="", **kwargs):
        """ always re-join channels {} """.format(channels)
        if command == '376':
            yield "JOIN {}".format(", ".join(channels))
        args = arguments.split(' ')
        if command == 'KICK' and self.config['nick'] in args[1]:
            yield "JOIN {}".format(args[0])
    return auto_join_closure
