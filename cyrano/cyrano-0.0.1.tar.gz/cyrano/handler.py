"""Stuff relating to app logic.
"""
import concurrent.futures
import threading
import logging


class _LoggerAdapter(logging.LoggerAdapter):
    # TODO: don't enforce this message format,
    # somehow provide flexibility
    # pref by reusing formatter on existing logger
    def process(self, msg, kwargs):
        family = self.extra['family']
        if family == "ipv4":
            line = '[%s:%s]->[%s:%s] %s' % (
                self.extra['remote_address'],
                self.extra['remote_port'],
                self.extra['local_address'],
                self.extra['local_port'],
                msg
            )
        elif family == "ipv6":
            line = '[%s]:%s -> [%s]:%s %s' % (
                self.extra['remote_address'],
                self.extra['remote_port'],
                self.extra['local_address'],
                self.extra['local_port'],
                msg
            )
        return line, kwargs


class _DummyExecutor(concurrent.futures.Executor):
    """Fake executor used when no other is provided.

    Used internal to this module to provide a point where a real
    executor could be substituted.
    """
    def __init__(self):
        super().__init__()

    def submit(self, function, *args, **kwargs):
        """Submit fake task to run synchronously.

        Note that exceptions which occur during execution are not
        suppressed and set on the future to simulate a real executor.
        They will just raise and stop execution to keep it simple.
        """
        future = concurrent.futures.Future()
        result = function(*args, **kwargs)
        future.set_result(result)
        return future


# TODO: do timeouts in a separate optional layer from this
class Handler(object):
    """Encapsulate a connection to a remote host from app's perspective.

    * Public API for use outside the iterator, allowing write and close.
    * Customization mechanism for per-connection state: subclasses can
      offer new methods and state if app needs these.
    * Abstracts an underlying network/event backend so the same app can
    be used on other backends and to discourage a spaghetti of low-level
    network concerns mashed up with app-level (Model) concerns.
    * Wraps an input-handling iterator so we can be event-driven using
    synchronous logic.
    Guards it in case people do something goofy which would garble
    input to it.

    This doesn't necessarily have to be TCP, same abstraction could
    perform a stateful sequence of UDP interactions against the same
    remote host.
    """
    # n.b.: this takes iterator so that can be instantiated in whatever
    # way, or recycled to resume an interrupted connection, etc.
    def __init__(self, iterator, write, close, info, logger=None):
        """
        :arg iterator:
            iterator implementing input handling.
            Whenever handler.receive is called with some bytes,
            those bytes are sent in and then the bytes yielded by
            the iterator are written over the network.
        :arg write:
            A callback which writes data to be sent to remote end.
        :arg close:
            A callback which closes the network connection.
        :arg info:
            A dict
        """
        self.external_write = write
        self.external_close = close
        self.info = info or {}
        self.iterator = iterator
        self.iterator_lock = threading.RLock()
        logger = logger or logging.getLogger('handler')
        # formatter = logging.Formatter('%(address)s %(port)s : %(message)s')
        # logger.setFormatter(formatter)
        adapter = _LoggerAdapter(logger, self.info)
        self.logger = adapter
        self.name = "conn"  # remove?
        self.remote_disconnect = None

    def connected(self):
        """Called to do setup after connection was made.
        """
        self.logger.info("connected")
        # prime iterator and collect bytes to write initially.
        initial = self.iterator.send(None)
        if initial:
            self.write(initial)

    def disconnected(self):
        """Called when the other side closed the connection.
        """
        self.logger.info("remote disconnect")
        self.remote_disconnect = True
        # n.b.: external_close has to be OK to call for dead connections
        self.close()

    def received(self, data):
        """Called when there is new data to handle.
        """
        self.logger.debug("received: %r", data)
        # Forward data to iterator and see what it wants to write.
        #   If it decides it's done, close connection.
        #   If it returned a value, send that before closing.
        # Locked because racing on iterator.send would be bad.
        # DON'T call close() inside the iterator_lock because it tries
        # to acquire it and will hang.
        should_close = False
        should_write = b""
        with self.iterator_lock:
            try:
                should_write = self.iterator.send(data)
            except StopIteration as stopped:
                should_write = stopped.value
                should_close = True
            if should_write:
                self.write(should_write)
        # If iterator advised writing something, write it.
        # if it said 'no comment,' don't bother.
        if should_close:
            self.close()

    def close(self):
        """Clean up own state and call the external close callback.
        """
        # n.b.: What the external close callback does is none of our
        # concern here, we just have to call it.
        # n.b.: this code will hang if iterator_lock is a Lock vs. an RLock,
        # because receive calls it when the iterator says to stop,
        # while receive still holds the lock.
        self.logger.debug("closing...")
        # Must close the iterator if it has a close, but some don't.
        # This throws GeneratorExit into the iterator at yield point.
        # If it catches GeneratorExit and returns, that's something it
        # wants us to write just like in receive().
        # For this reason, external_close has to be called after iterator
        # has been closed.
        with self.iterator_lock:
            self.logger.debug("holding iterator_lock")
            if hasattr(self.iterator, "close"):
                self.logger.debug("closing iterator")
                try:
                    self.iterator.close()
                except StopIteration as stopped:
                    if stopped.value:
                        self.write(stopped.value)
        self.logger.debug("calling external_close")
        self.external_close(self)
        self.logger.debug("closed.")

    def write(self, data):
        assert isinstance(data, bytes), "arg to write is not bytes"
        self.external_write(data)

    @classmethod
    def factory(cls, generator):
        """Make a function returning instances for the given generator.
        """
        # n.b.: different classes can provide their own factory methods
        # accounting for their own interfaces
        def handler_factory(write, close, info):
            """Return bound handler instances.
            """
            iterator = generator()
            handler = cls(iterator, write, close, info)
            return handler

        return handler_factory


class HandlerSet(object):
    """Keep track of some handler instances.

    The primary use is to make sure the handlers can be closed later,
    allowing them to do their own cleanups (including closing actual
    network connections). It can also be useful to iterate over
    handlers for other reasons.

    This shouldn't know or care what sort of objects are being used as
    handlers.
    """
    # note to self:
    # In some ways like old Cyrano's Acceptor. But unlike Acceptor, this
    # doesn't take a listen socket, close it, call accept, or register
    # new socket fd activity to call a method on the handler.
    # register and unregister become utility callbacks so other
    # components can track handlers, rather than methods for setting up
    # fd watches.
    # - so far, does not make connections either. which is logical if
    # it's not doing accepts;
    # but it means something else has to make the handler instance,
    # passing in
    # handlerset.remove to its constructor, and call
    # handlerset.add to get the ball rolling.
    # - This doesn't implement the Python set interface because it's
    # really only for a limited set of operations.
    def __init__(self, logger=None):
        """
        """
        logger = logger or logging.getLogger()
        self.logger = logger.getChild(self.__class__.__name__)
        self.handlers = set()
        self.executor = _DummyExecutor()
        self.lock = threading.Lock()

    def __iter__(self):
        """Provide an iterator view on the current handlers.

        Recommended usage: 'for handler in handlerset:'

        Assuming add and remove are called in a timely way, the results
        should be handlers which were recently alive. But it isn't
        guaranteed that they are still live, since a handler may be
        removed from the set after the call to __iter__ but before that
        handler is yielded.
        In other words, this snapshots the set at the time the iterator
        is made. This avoids errors or locking to avoid those errors,
        but it means caller is responsible for dealing with the cases
        where the connection it gets was removed after the iterator was
        made, or something was added after the iterator was made.
        """
        handlers = self.handlers.copy()
        for handler in handlers:
            yield handler

    def __len__(self):
        return len(self.handlers)

    def add(self, handler):
        """Track the given handler instance.
        """
        with self.lock:
            self.handlers.add(handler)

    def remove(self, handler):
        """Forget the given handler instance.

        Closing handlers should call this method so we can update,
        implying that it is passed as a callback to the handler.
        """
        # Don't race with pending operations.
        with self.lock:
            # Don't raise or dawdle if we are in a HandlerSet close.
            if not self.handlers:
                return False
            # Don't raise if handler was not in our set.
            try:
                self.handlers.remove(handler)
            except KeyError:
                pass
        # n.b.: this should not call handler.close(); that should be
        # done either by handler-driven events, or by
        # HandlerSet.close

    def close(self, timeout=None):
        """Clean up any handlers tracked by this handlerset.

        This is a top-down shutdown of current handlers, as opposed
        to event-driven handler.close calls.

        If a close is already in progress in another thread, the call
        should fail immediately.

        Otherwise, this should block until the handlers are all closed.

        This shouldn't be called until external adds and removes have
        been prevented, or the external caller is likely to be
        surprised.
        """
        # To avoid contention on the self.handlers set by lots of remove
        # calls, get the set to myself; we'll soon clear it out at all
        # at once (obviating need for any remove calls)
        with self.lock:
            handlers = self.handlers
            # If another thread is already closing, don't hold up progress in
            # this one til they are done, it might be a while.
            if handlers is None:
                self.logger.debug("already closing")
                return
            self.handlers = None

        # Ask handlers to close themselves. If closes take significant time
        # and/or there are a large number to do, may be worth trying
        # a different executor to do this in parallel.
        # n.b.: don't want this done inside the lock, because then other
        # calls to close will block.
        self.logger.debug("closing handlers")
        close_futures = [
            self.executor.submit(handler.close)
            for handler in handlers
        ]
        done, pending = concurrent.futures.wait(close_futures, timeout=timeout)
        if pending:
            self.logger.warning("%d handlers unclosed", len(pending))
        self.logger.debug("closed %d handlers", len(done))


class App(object):
    """Home of any API and state to be shared across handlers.

    Calls into this API are the only way an App instance should be able
    to get involved in responding to input.
    """
    def __init__(self, generator, logger=None):
        self.logger = logger or logging.getLogger(self.__class__.__name__)
        self.handlers = HandlerSet(logger=self.logger)
        self.handler_factory = Handler.factory(generator)
    # n.b.: handler_factory knows the generator so we don't have to.
    # HandlerSet should not need to know about the factory.

    def new_handler(self, write, close, info):
        """Respond to new connection.

        Provides own notification callbacks to the new handler.
        """
        def new_close(handler):
            """Close connection and tell app that this handler closed.

            This is passed to the Handler as its external_close and
            should be called whenever handler.close is called.
            It isn't meant to call handler.close.
            """
            self.closed(handler)
            close()

        handler = self.handler_factory(write, new_close, info)
        self.connected(handler)
        return handler

    def connected(self, handler):
        """Called to notify app of new connection.
        """
        handler.logger.debug("remote connected!")
        self.handlers.add(handler)

    def closed(self, handler):
        """Called to notify app of lost connection.

        This method just defines how the app responds to handler going away.
        It isn't responsible to close the handler or the connection.
        The handler is responsible to close itself and call its external
        close callback; that callback is responsible to close the
        connection and call this.
        """
        if handler.remote_disconnect:
            handler.logger.debug("remote disconnected!")
        self.handlers.remove(handler)

    def close(self):
        """Initiate a shutdown across all handlers.
        """
        self.handlers.close()
