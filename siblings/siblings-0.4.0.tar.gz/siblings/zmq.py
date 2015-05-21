from __future__ import absolute_import, division, print_function
from abc import abstractmethod, ABCMeta
import time
import logging
import multiprocessing
import threading
from binascii import hexlify

import zmq




# Code of this module adapted Majordomo Protocol form zmq guide
# (http://zguide.zeromq.org/)

class MDP(object):
    """Majordomo Protocol definitions"""
    #  This is the version of MDP/Client we implement
    C_CLIENT = "MDPC01"

    #  This is the version of MDP/Worker we implement
    W_WORKER = "MDPW01"

    #  MDP/Server commands, as strings
    W_READY         =   b"\001"
    W_REQUEST       =   b"\002"
    W_REPLY         =   b"\003"
    W_HEARTBEAT     =   b"\004"
    W_DISCONNECT    =   b"\005"

    commands = [None, "READY", "REQUEST", "REPLY", "HEARTBEAT", "DISCONNECT"]


class Service(object):
    """A container to hold information on a single Service"""
    def __init__(self, name):
        self.name = name
        self.requests = []
        self.waiting = []


class Worker(object):
    """A container which holds information for a single Worker.
    The worker can be idle or active"""
    identity = None # hex Identity of worker
    address = None # Address to route to
    service = None # Owning service, if known
    expiry = None # expires at this point, unless heartbeat

    def __init__(self, identity, address, lifetime):
        self.identity = identity
        self.address = address
        self.expiry = time.time() + 1e-3*lifetime


class MajorDomoBase(object):
    """
    Majordomo Protocol Base class, defining common consts.
    A minimal implementation of http:#rfc.zeromq.org/spec:7 and spec:8
    """

    __metaclass__ = ABCMeta
    HEARTBEAT_LIVENESS = 3 # 3-5 is reasonable
    HEARTBEAT_INTERVAL = 5000  # msecs
    HEARTBEAT_EXPIRY = HEARTBEAT_INTERVAL * HEARTBEAT_LIVENESS

    # ---------------------------------------------------------------------
    context_factory = zmq.Context.instance
    # ---------------------------------------------------------------------
    def __init__(self, verbose=False):
        """Initialize broker state."""
        self.verbose = verbose
        self._binds = []
        self._connects = []
        self._sockopts = []
        self._mon_binds = []
        self._mon_sockopts = []
        self.daemon = True
        self.done = False
        self.data_socket = None
        self.setsockopt(zmq.LINGER, 0)
        logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S",
                level=logging.INFO)

    def init_in_subprocess(self):
        self._setup_sockets()

    def _setup_sockets(self):
        ctx = self.context_factory()
        self.ctx = ctx

        # create the sockets
        data_sock = ctx.socket(self.data_socket_type)

        # set sockopts (must be done first, in case of zmq.IDENTITY)
        for opt, value in self._sockopts:
            data_sock.setsockopt(opt, value)
        for iface in self._binds:
            data_sock.bind(iface)
        for iface in self._connects:
            data_sock.connect(iface)

        if len(self._mon_binds) > 0:
            mon = ctx.socket(zmq.PUB)
            for opt, value in self._mon_sockopts:
                mon.setsockopt(opt, value)
            for iface in self._mon_binds:
                mon.bind(iface)
        else:
            mon = None
        self.data_socket = data_sock
        self.mon_socket = mon

    def run(self):
        """wrap run_broker in try/catch ETERM"""
        try:
            self.init_in_subprocess()
            self.run_device()
        except zmq.ZMQError as e:
            if e.errno == zmq.ETERM:
                # silence TERM errors, because this should be a clean shutdown
                pass
            else:
                raise
        finally:
            self.done = True

    def start(self):
        """Start the device. Override me in subclass for other launchers."""
        return self.run()

    def join(self,timeout=None):
        """wait for me to finish, like Thread.join.

        Reimplemented appropriately by subclasses."""
        tic = time.time()
        toc = tic
        while not self.done and not (timeout is not None and toc-tic > timeout):
            time.sleep(.001)
            toc = time.time()

    @abstractmethod
    def run_device(self):
        pass

    def bind(self, endpoint):
        """Bind device to endpoint, can call this multiple times.
        We use a single socket for both clients and workers.
        """
        self._binds.append(endpoint)

    def connect(self, endpoint):
        """Connect device to endpoint, can call this multiple times."""
        self._connects.append(endpoint)

    def setsockopt(self, opt, value):
        """Enqueue setsockopt(opt, value) for data socket
        See zmq.Socket.setsockopt for details.
        """
        self._sockopts.append((opt, value))

    def bind_mon(self, endpoint):
        """Bind monitor of broker to endpoint, can call this multiple times.
        """
        self._mon_binds.append(endpoint)

    def setsockopt_mon(self, opt, value):
        """Enqueue setsockopt(opt, value) for monitor socket
        See zmq.Socket.setsockopt for details.
        """
        self._sockopts.append((opt, value))

    def send_msg_to_monitors(self, msg):
        """send any message to the monitors if mon_socket exists"""
        if not self.mon_socket is None:
            self.mon_socket.send_multipart(msg)


class MajorDomoBroker(MajorDomoBase):
    """
    Majordomo Protocol broker, base implementation.
    A minimal implementation of http:#rfc.zeromq.org/spec:7 and spec:8
    """
    INTERNAL_SERVICE_PREFIX = "mmi."

    def __init__(self, verbose=False):
        """Initialize broker state."""
        super(MajorDomoBroker, self).__init__(verbose)
        self.data_socket_type = zmq.ROUTER
        self.services = {}
        self.workers = {}
        self.waiting = []
        self.heartbeat_at = time.time() + 1e-3*self.HEARTBEAT_INTERVAL

    def run_device(self):
        poller = zmq.Poller()
        poller.register(self.data_socket, zmq.POLLIN)

        """Main broker work happens here"""
        while True:
            try:
                items = poller.poll(self.HEARTBEAT_INTERVAL)
            except KeyboardInterrupt:
                break  # Interrupted
            if items:
                msg = self.data_socket.recv_multipart()
                if self.verbose:
                    logging.info("I: received message: {}".format(msg))
                    #dump(msg)

                sender = msg.pop(0)
                empty = msg.pop(0)
                assert empty == b''
                header = msg.pop(0)

                if MDP.C_CLIENT == header:
                    self.process_client(sender, msg)
                elif MDP.W_WORKER == header:
                    self.process_worker(sender, msg)
                else:
                    logging.error("E: invalid message:")
                    #dump(msg)

            self.purge_workers()
            self.send_heartbeats()

    def destroy(self):
        """Disconnect all workers, destroy context."""
        while self.workers:
            self.delete_worker(self.workers[0], True)
        self.ctx.destroy(0)


    def process_client(self, sender, msg):
        """Process a request coming from a client."""
        assert len(msg) >= 2 # Service name + body
        service = msg.pop(0)
        # Set reply return address to client sender
        msg = [sender, b''] + msg
        if service.startswith(self.INTERNAL_SERVICE_PREFIX):
            self.service_internal(service, msg)
        else:
            self.dispatch(self.require_service(service), msg)


    def process_worker(self, sender, msg):
        """Process message sent to us by a worker."""
        assert len(msg) >= 1  # At least, command is expected
        command = msg.pop(0)
        worker_ready = hexlify(sender) in self.workers
        worker = self.require_worker(sender)

        if MDP.W_READY == command:
            assert len(msg) >= 1  # At least, a service name
            service = msg.pop(0)
            # Not first command in session or Reserved service name
            if worker_ready or service.startswith(self.INTERNAL_SERVICE_PREFIX):
                self.delete_worker(worker, True)
            else:
                # Attach worker to service and mark as idle
                worker.service = self.require_service(service)
                self.worker_waiting(worker)

        elif MDP.W_REPLY == command:
            if worker_ready:
                # Remove & save client return envelope and insert the
                # protocol header and service name, then rewrap envelope.
                client = msg.pop(0)
                empty = msg.pop(0)
                msg = [client, b'', MDP.C_CLIENT, worker.service.name] + msg
                if self.verbose:
                    logging.info('sending reply {0!r} to client {1!r}'.format(MDP.C_CLIENT, client))
                self.data_socket.send_multipart(msg)
                self.worker_waiting(worker)
            else:
                self.delete_worker(worker, True)

        elif MDP.W_HEARTBEAT == command:
            if worker_ready:
                worker.expiry = time.time() + 1e-3*self.HEARTBEAT_EXPIRY
            else:
                self.delete_worker(worker, True)

        elif MDP.W_DISCONNECT == command:
            self.delete_worker(worker, False)
        else:
            logging.error("E: invalid message:")
            #dump(msg)

    def delete_worker(self, worker, disconnect):
        """Deletes worker from all data structures, and deletes worker."""
        assert worker is not None
        if disconnect:
            self.send_to_worker(worker, MDP.W_DISCONNECT, None, None)

        if worker.service is not None:
            worker.service.waiting.remove(worker)
        self.workers.pop(worker.identity)

    def require_worker(self, address):
        """Finds the worker (creates if necessary)."""
        assert (address is not None)
        identity = hexlify(address)
        worker = self.workers.get(identity)
        if worker is None:
            worker = Worker(identity, address, self.HEARTBEAT_EXPIRY)
            self.workers[identity] = worker
            if self.verbose:
                logging.info("I: registering new worker: %s", identity)

        return worker

    def require_service(self, name):
        """Locates the service (creates if necessary)."""
        assert (name is not None)
        service = self.services.get(name)
        if service is None:
            service = Service(name)
            self.services[name] = service

        return service

    def service_internal(self, service, msg):
        """Handle internal service according to 8/MMI specification"""
        returncode = "501"
        if "mmi.service" == service:
            name = msg[-1]
            returncode = "200" if name in self.services else "404"
        msg[-1] = returncode

        # insert the protocol header and service name after the routing envelope ([client, ''])
        msg = msg[:2] + [MDP.C_CLIENT, service] + msg[2:]
        self.data_socket.send_multipart(msg)

    def send_heartbeats(self):
        """Send heartbeats to idle workers if it's time"""
        if time.time() > self.heartbeat_at:
            for worker in self.waiting:
                self.send_to_worker(worker, MDP.W_HEARTBEAT, None, None)

            self.heartbeat_at = time.time() + 1e-3*self.HEARTBEAT_INTERVAL

    def purge_workers(self):
        """Look for & kill expired workers.

        Workers are oldest to most recent, so we stop at the first alive worker.
        """
        while self.waiting:
            w = self.waiting[0]
            if w.expiry < time.time():
                logging.info("I: deleting expired worker: %s", w.identity)
                self.delete_worker(w,False)
                self.waiting.pop(0)
            else:
                break

    def worker_waiting(self, worker):
        """This worker is now waiting for work."""
        # Queue to broker and service waiting lists
        self.waiting.append(worker)
        worker.service.waiting.append(worker)
        worker.expiry = time.time() + 1e-3*self.HEARTBEAT_EXPIRY
        self.dispatch(worker.service, None)

    def dispatch(self, service, msg):
        """Dispatch requests to waiting workers as possible"""
        assert (service is not None)
        if msg is not None:  # Queue message if any
            service.requests.append(msg)
        self.purge_workers()
        while service.waiting and service.requests:
            msg = service.requests.pop(0)
            worker = service.waiting.pop(0)
            self.waiting.remove(worker)
            self.send_to_worker(worker, MDP.W_REQUEST, None, msg)

    def send_to_worker(self, worker, command, option, msg=None):
        """Send message to worker.

        If message is provided, sends that message.
        """

        if msg is None:
            msg = []
        elif not isinstance(msg, list):
            msg = [msg]

        # Stack routing and protocol envelopes to start of message
        # and routing envelope
        if option is not None:
            msg = [option] + msg
        msg = [worker.address, '', MDP.W_WORKER, command] + msg

        if self.verbose:
            logging.info("I: sending {!r} to worker {!r}".format(command, worker.address))

        self.data_socket.send_multipart(msg)


class BackgroundMajorDomoBroker(MajorDomoBroker):
    """Base class for launching Devices in background processes and threads."""

    launcher = None
    _launch_class = None

    def start(self):
        self.launcher = self._launch_class(target=self.run)
        self.launcher.daemon = self.daemon
        return self.launcher.start()

    def join(self, timeout=None):
        return self.launcher.join(timeout=timeout)


class ThreadMajorDomoBroker(BackgroundMajorDomoBroker):
    """A Device that will be run in a background Thread.

    See Device for details.
    """
    _launch_class=threading.Thread

class ProcessMajorDomoBroker(BackgroundMajorDomoBroker):
    """A Device that will be run in a background Process.

    See Device for details.
    """
    _launch_class=multiprocessing.Process
    context_factory = zmq.Context
    """Callable that returns a context. Typically either Context.instance or Context,
    depending on whether the device should share the global instance or not.
    """



class MajorDomoWorker(MajorDomoBase):
    """Majordomo Protocol Worker API, Python version

    Implements the MDP/Worker spec at http:#rfc.zeromq.org/spec:7.
    """

    def __init__(self, broker_url, service, verbose=False):
        super(MajorDomoWorker, self).__init__(verbose)
        self.RECONNECT_INTERVAL = 2*self.HEARTBEAT_INTERVAL
        self.data_socket_type = zmq.DEALER
        self.connect(broker_url)
        self.service = service
        self.expect_reply = False
        self.reply_to = None
        self.timeout = self.HEARTBEAT_INTERVAL

    def init_in_subprocess(self):
        self.poller = zmq.Poller()
        self.reconnect_to_broker()

    def reconnect_to_broker(self):
        """Connect or reconnect to broker"""
        if self.data_socket:
            self.poller.unregister(self.data_socket)
            self.data_socket.close()
        self._setup_sockets()
        self.poller.register(self.data_socket, zmq.POLLIN)
        if self.verbose:
            logging.info("I: connecting to broker")

        # Register service with broker
        self.send_to_broker(MDP.W_READY, self.service, None)

        # If liveness hits zero, queue is considered disconnected
        self.liveness = self.HEARTBEAT_LIVENESS
        self.heartbeat_at = time.time() + 1e-3 * self.HEARTBEAT_INTERVAL


    def send_to_broker(self, command, option=None, msg=None):
        """Send message to broker.

        If no msg is provided, creates one internally
        """
        if msg is None:
            msg = []
        elif not isinstance(msg, list):
            msg = [msg]

        if option:
            msg = [option] + msg

        msg = ['', MDP.W_WORKER, command] + msg
        if self.verbose:
            logging.info("sending {!r} to broker".format(command))
        self.data_socket.send_multipart(msg)


    def recv(self, reply=None):
        """Send reply, if any, to broker and wait for next request."""
        # Format and send the reply if we were provided one
        assert reply is not None or not self.expect_reply

        if reply is not None:
            assert self.reply_to is not None
            reply = [self.reply_to, ''] + reply
            self.send_to_broker(MDP.W_REPLY, msg=reply)

        self.expect_reply = True

        while True:
            # Poll socket for a reply, with timeout
            items = self.poller.poll(self.timeout)
            if items:
                msg = self.data_socket.recv_multipart()

                self.liveness = self.HEARTBEAT_LIVENESS
                # Don't try to handle errors, just assert noisily
                assert len(msg) >= 3
                empty = msg.pop(0)
                assert empty == ''
                header = msg.pop(0)
                assert header == MDP.W_WORKER
                command = msg.pop(0)

                if self.verbose:
                    logging.info("received message ({!r}) from broker".format(command))
                if command == MDP.W_REQUEST:
                    # We should pop and save as many addresses as there are
                    # up to a null part, but for now, just save one...
                    self.reply_to = msg.pop(0)
                    # pop empty
                    assert msg.pop(0) == ''
                    return msg  # We have a request to process
                elif command == MDP.W_HEARTBEAT:
                    # Do nothing for heartbeats
                    pass
                elif command == MDP.W_DISCONNECT:
                    self.reconnect_to_broker()
                else:
                    logging.error("invalid input message received. command: {!r}, msg: {!r}".format(command, msg))

            else:
                self.liveness -= 1
                if self.liveness == 0:
                    if self.verbose:
                        logging.warn("disconnected from broker - retrying...")
                    time.sleep(1e-3*self.RECONNECT_INTERVAL)
                    self.reconnect_to_broker()

            # Send HEARTBEAT if it's time
            if time.time() > self.heartbeat_at:
                self.send_to_broker(MDP.W_HEARTBEAT)
                self.heartbeat_at = time.time() + 1e-3*self.HEARTBEAT_INTERVAL

        return None

    def destroy(self):
        # context.destroy depends on pyzmq >= 2.1.10
        self.ctx.destroy(0)


class BackgroundMajorDomoWorker(MajorDomoWorker):
    """Base class for launching Devices in background processes and threads."""

    launcher = None
    _launch_class = None

    def start(self):
        self.launcher = self._launch_class(target=self.run)
        self.launcher.daemon = self.daemon
        return self.launcher.start()

    def join(self, timeout=None):
        return self.launcher.join(timeout=timeout)


class ThreadMajorDomoWorker(BackgroundMajorDomoWorker):
    """A Device that will be run in a background Thread.

    See Device for details.
    """
    _launch_class=threading.Thread

class ProcessMajorDomoWorker(BackgroundMajorDomoWorker):
    """A Device that will be run in a background Process.

    See Device for details.
    """
    _launch_class=multiprocessing.Process
    context_factory = zmq.Context


class MajorDomoClient(MajorDomoBase):
    """Majordomo Protocol Client API, Python version.

      Implements the MDP/Worker spec at http:#rfc.zeromq.org/spec:7.
    """

    def __init__(self, broker, verbose=False):
        super(MajorDomoClient, self).__init__(verbose)
        self.connect(broker)
        self.data_socket_type = zmq.DEALER
        self.timeout = 100

    def init_in_subprocess(self):
        self.poller = zmq.Poller()
        self.reconnect_to_broker()

    def reconnect_to_broker(self):
        """Connect or reconnect to broker"""
        if self.data_socket:
            self.poller.unregister(self.data_socket)
            self.data_socket.close()
        self._setup_sockets()
        self.poller.register(self.data_socket, zmq.POLLIN)
        logging.info("I: connecting to broker at %s...", self._connects[0])

    def send(self, service, request):
        """Send request to broker
        """
        if not isinstance(request, list):
            request = [request]

        # Prefix request with protocol frames
        # Frame 0: empty (REQ emulation)
        # Frame 1: "MDPCxy" (six bytes, MDP/Client x.y)
        # Frame 2: Service name (printable string)

        request = ['', MDP.C_CLIENT, service] + request
        if self.verbose:
            logging.info("I: send request to '%s' service: ", service)
        self.data_socket.send_multipart(request)

    def recv(self):
        """Returns the reply message or None if there was no reply."""
        items = self.poller.poll(self.timeout)

        if items:
            # if we got a reply, process it
            msg = self.data_socket.recv_multipart()
            if self.verbose:
                logging.info("I: received reply:")

            # Don't try to handle errors, just assert noisily
            assert len(msg) >= 4

            empty = msg.pop(0)
            header = msg.pop(0)
            assert MDP.C_CLIENT == header

            service = msg.pop(0)
            return msg
        else:
            if self.verbose:
                logging.info("W: no reply received")


class BackgroundMajorDomoClient(MajorDomoClient):
    """Base class for launching Devices in background processes and threads."""

    launcher = None
    _launch_class = None

    def start(self):
        self.launcher = self._launch_class(target=self.run)
        self.launcher.daemon = self.daemon
        return self.launcher.start()

    def join(self, timeout=None):
        return self.launcher.join(timeout=timeout)


class ThreadMajorDomoClient(BackgroundMajorDomoClient):
    """A Device that will be run in a background Thread.

    See Device for details.
    """
    _launch_class=threading.Thread

class ProcessMajorDomoClient(BackgroundMajorDomoClient):
    """A Device that will be run in a background Process.

    See Device for details.
    """
    _launch_class=multiprocessing.Process
    context_factory = zmq.Context


__all__ = ['ThreadMajorDomoBroker', 'ProcessMajorDomoBroker', 'MajorDomoBroker', 'MajorDomoWorker',
           'ProcessMajorDomoWorker', 'ThreadMajorDomoWorker', 'MajorDomoClient', 'ThreadMajorDomoClient',
           'ProcessMajorDomoClient']
