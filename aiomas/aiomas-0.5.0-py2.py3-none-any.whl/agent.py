"""
This module implements the base class for agents (:class:`Agent`) and
containers for agents (:class:`Container`).

Every agent must live in a container.  A container can contain one ore more
agents.  Containers are responsible for making connections to other containers
and agents.  They also provide a factory function for spawning new agent
instances and registering them with the container.

Thus, the :class:`Agent` base class is very light-weight.  It only has a name,
a reference to its container and an RPC router (see :mod:`aiomas.rpc`).

"""
import asyncio
import weakref
import socket

import aiomas.channel
import aiomas.codecs
import aiomas.clocks
import aiomas.rpc
import aiomas.util

__all__ = ['Container', 'Agent']


PROTOCOLS = {
    'tcp',  # TCP sockets
    'ipc',  # Inter Process Communication with Unix domain sockets
}


class Container:
    """Container for agents.

    It can instantiate new agents via :meth:`spawn()` and can create
    connections to other agents (via :meth:`connect()`).

    In order to destroy a container and close all of its sockets, call
    :meth:`shutdown()`.

    When a container is created, it also creates a server socket and binds it
    to *addr* which is a ``('host', port)`` tuple (see the *host* and *port*
    parameters of :meth:`asyncio.BaseEventLoop.create_server()` for details).

    You can optionally also pass a *codec* class.  Note that containers can
    only "talk" to containers using the same codec.

    You can also pass a list of *extra_serializers* for the codec.  The list
    entires need to be callables that return a tuple with the arguments for
    :meth:`~aiomas.codecs.Codec.add_serializer()`.

    To decouple a multi-agent system from the system clock, you can pass an
    optional *clock* object which should be an instance of
    :class:`~aiomas.clocks.BaseClock`.  This makes it easier to integrate your
    system with other simulators that may provide a clock for you or to let
    your MAS run as fast as possible.  By default,
    :class:`~aiomas.clocks.AsyncioClock` will be used.

    """

    router = aiomas.rpc.Service(['agents'])

    def __init__(self, addr, clock=None, codec=None, extra_serializers=()):
        if codec is None:
            codec = aiomas.channel.DEFAULT_CODEC
        if clock is None:
            clock = aiomas.clocks.AsyncioClock()

        self._addr = addr
        self._codec = codec
        self._extra_serializers = [aiomas.clocks.arrow_serializer]
        self._extra_serializers += extra_serializers
        self._clock = clock

        # Set a sensbile hostname
        if type(addr) is tuple:
            if addr[0] in [None, '', '::', '0.0.0.0']:
                # Use the FQDN if we bind to all interfaces
                self._host = socket.getfqdn()
            else:
                # Use the IP address or host name if not
                self._host = addr[0]
            self._port = addr[1]
        else:
            self._host = None
            self._port = None

        # The agents managed by this container.
        # The agents' routers are subrouters of the container's root router.
        self.agents = aiomas.rpc.RoutingDict()

        # RPC service for this container
        self._tcp_server = None
        self._rpc_cons = set()
        self._tcp_server_started = aiomas.util.async(self._start_tcp_server())

        # Caches
        self._connections_out_futs = {}  # Futures for outgoing connections
        self._connections_out = {}  # RPC connections to containers by address
        self._remote_agent_futs = {}  # Futures for remote agent validation
        self._remote_agents = {}  # Validated remote agents by connection

    def __str__(self):
        return '%s(%r, %s, %s)' % (self.__class__.__name__, self._addr,
                                   self._clock.__class__.__name__,
                                   self._codec.__name__)

    @property
    def codec(self):
        """The codec used by this container.  Instance of
        :class:`aiomas.codecs.Codec`."""
        return self._codec

    @property
    def clock(self):
        """The clock of the container.  Instance of
        :class:`aiomas.clocks.BaseClock`."""
        return self._clock

    def spawn(self, agent_type, *args, **kwargs):
        """Create an instance of *agent_type*, passing a reference to this
        container, a name and the provided *args* and **kwargs** to it.

        This is equivalent to ``agent = agent_type(container, name, *args,
        **kwargs)``, but also registers the agent with the container.

        """
        aid = str(len(self.agents.dict))
        if self._host is None:
            url = '%s://[%s]/%s' % ('ipc', self._addr, aid)
        else:
            url = '%s://%s:%s/%s' % ('tcp', self._host, self._port, aid)

        agent = agent_type(self, url, *args, **kwargs)
        self.agents.dict[aid] = agent
        self.agents.router.set_sub_router(agent.router, aid)
        return agent

    @asyncio.coroutine
    def connect(self, url):
        """Connect to the argent available at *url* and return a proxy to it.

        *url* is a string ``<protocol>://<addr>//<agent-id>`` (e.g.,
        ``'tcp://localhost:5555/0'``).

        """
        addr, aid = self._parse_url(url)

        rpc_con = yield from self._open_connection(addr)
        remote_agent = yield from self._validate_aid(aid, rpc_con, addr, url)

        return remote_agent

    def shutdown(self, async=False):
        """Close the container's server socket and the RPC services for all
        outgoing TCP connections.

        If *async* is left to ``False``, this method calls
        :meth:`asyncio.BaseEventLoop.run_until_complete()` in order to wait
        until all sockets are closed.

        If the event loop is already running when you call this method, set
        *async* to ``True``. The return value then is a coroutine that you need
        to ``yield from`` in order to actually shut the container down::

            yield from container.shutdown(async=True)

        """
        @asyncio.coroutine
        def _shutdown():
            # Wait until the TCP server is up before trying to terminate it.
            # self._tcp_server is None until this task is finished!
            yield from self._tcp_server_started

            if self._tcp_server:
                # Request closing the server socket and cancel the services
                self._tcp_server.close()
                for con in self._rpc_cons:
                    con.service.cancel()

                # Close all outgoing connections
                for con in self._connections_out.values():
                    con.close()

                # Wait for server and services to actually terminate
                yield from asyncio.gather(self._tcp_server.wait_closed(),
                                          *[c.service for c in self._rpc_cons])

                self._tcp_server = None
                self._rpc_cons = None

        if async:
            return _shutdown()
        else:
            asyncio.get_event_loop().run_until_complete(_shutdown())

    @router.expose
    def validate_aid(self, aid):
        """Return the class name for the agent represented by *aid* if it
        exists or ``None``."""
        agents = self.agents.dict
        if aid in agents:
            return agents[aid].__class__.__name__

    @asyncio.coroutine
    def _start_tcp_server(self):
        """Helper task to create an RPC server for this container."""
        def add_to_con_cache(rpc):
            self._rpc_cons.add(rpc)

        self._tcp_server = yield from aiomas.rpc.start_server(
            self._addr,
            self.router,
            client_connected_cb=add_to_con_cache,
            codec=self._codec,
            extra_serializers=self._extra_serializers)

    def _parse_url(self, url):
        """Parse the agent *url* and return a ``((host, port), agent)`` tuple.

        Raise a :exc:`ValueError` if the URL cannot be parsed.

        """
        try:
            proto, addr_aid = url.split('://', 1)
            assert proto in PROTOCOLS, '%s not in %s' % (proto, PROTOCOLS)

            if proto == 'tcp':
                addr, aid = addr_aid.split('/', 1)
                host, port = addr.rsplit(':', 1)
                if host[0] == '[' and host[-1] == ']':
                    # IPv6 addresses may be surrounded by []
                    host = host[1:-1]
                addr = (host, int(port))

            elif proto == 'ipc':
                assert addr_aid[0] == '['
                addr, aid = addr_aid[1:].split(']/', 1)

            assert aid, 'No agent ID specified.'

        except (AssertionError, IndexError, ValueError) as e:
            raise ValueError('Cannot parse agent URL "%s": %s' % (url, e))

        return addr, aid

    @asyncio.coroutine
    def _open_connection(self, addr):
        if addr in self._connections_out:
            # Return cached connection
            rpc_con = self._connections_out[addr]
        elif addr in self._connections_out_futs:
            # Wait for ongoing connection attempt
            rpc_con = yield from self._connections_out_futs[addr]
        else:
            # Open new connection
            fut = asyncio.Future()
            self._connections_out_futs[addr] = fut

            rpc_con = yield from aiomas.rpc.open_connection(
                addr,
                router=self.router,
                codec=self._codec,
                extra_serializers=self._extra_serializers)

            # Put connection into the cache
            self._rpc_cons.add(rpc_con)
            self._connections_out[addr] = rpc_con

            # Trigger future and remove it from the cache
            fut.set_result(rpc_con)
            self._connections_out_futs.pop(addr)

            # Initialize caches for remote agents
            self._remote_agents[rpc_con] = weakref.WeakValueDictionary()
            self._remote_agent_futs[rpc_con] = {}

        return rpc_con

    @asyncio.coroutine
    def _validate_aid(self, aid, rpc_con, addr, url):
        remote_agents = self._remote_agents[rpc_con]
        remote_agent_futs = self._remote_agent_futs[rpc_con]

        if aid in remote_agents:
            remote_agent = remote_agents[aid]
        elif aid in remote_agent_futs:
            remote_agent = yield from remote_agent_futs[aid]
        else:
            fut = asyncio.Future()
            remote_agent_futs[aid] = fut

            remote_type = yield from rpc_con.remote.validate_aid(aid)
            if remote_type is None:
                raise ConnectionError('Agent "%s" does not exist in '
                                      'Container(%r)' % (aid, addr))
            remote_agent = getattr(rpc_con.remote.agents, aid)
            remote_agent._str = '%sProxy(%r)' % (remote_type, url)

            remote_agents[aid] = remote_agent
            fut.set_result(remote_agent)
            remote_agent_futs.pop(aid)

        return remote_agent


class Agent:
    """Base class for all agents."""

    router = aiomas.rpc.Service()
    """Descriptor that creates an RPC :class:`~aiomas.rpc.Router` for every
    agent instance.

    You can override this in a sub-class if you need to.  (Usually, you don't.)

    """
    def __init__(self, container, addr):
        if type(container) != Container:
            raise TypeError('"container" must be a "Container" instance but '
                            'is %s' % container)

        self.__container = container
        self.__addr = addr
        self.__name = '%s(%r)' % (self.__class__.__name__, addr)

    def __str__(self):
        return self.__name

    @property
    def container(self):
        """The :class:`Container` that the agent lives in."""
        return self.__container

    @property
    def addr(self):
        """The agent's address."""
        return self.__addr
