from rx import Lock
from rx.observable import Observable
from rx.internal import DisposedException
from rx.disposables import Disposable
from rx.abstractobserver import AbstractObserver

from .innersubscription import InnerSubscription


class BehaviorSubject(Observable, AbstractObserver):
    """Represents a value that changes over time. Observers can subscribe to
    the subject to receive the last (or initial) value and all subsequent
    notifications.
    """

    def __init__(self, value):
        """Initializes a new instance of the BehaviorSubject class which
        creates a subject that caches its last value and starts with the
        specified value.

        Keyword parameters:
        :param T value: Initial value sent to observers when no other value has
            been received by the subject yet.
        """

        super(BehaviorSubject, self).__init__(self.__subscribe)

        self.value = value
        self.observers = []
        self.is_disposed = False
        self.is_stopped = False
        self.exception = None

        self.lock = Lock()

    def check_disposed(self):
        if self.is_disposed:
            raise DisposedException()

    def __subscribe(self, observer):
        ex = None

        with self.lock:
            self.check_disposed()
            if not self.is_stopped:
                self.observers.append(observer)
                observer.on_next(self.value)
                return InnerSubscription(self, observer)
            ex = self.exception

        if ex:
            observer.on_error(ex)
        else:
            observer.on_completed()

        return Disposable.empty()

    def on_completed(self):
        """Notifies all subscribed observers of the end of the sequence."""

        os = None
        with self.lock:
            self.check_disposed()
            if not self.is_stopped:
                os = self.observers[:]
                self.observers = []
                self.is_stopped = True

        if os:
            for o in os:
                o.on_completed()


    def on_error(self, error):
        """Notifies all subscribed observers with the exception."""

        os = None
        with self.lock:
            self.check_disposed()
            if not self.is_stopped:
                os = self.observers[:]
                self.observers = []
                self.is_stopped = True
                self.exception = error

        if os:
            for o in os:
                o.on_error(error)

    def on_next(self, value):
        """Notifies all subscribed observers with the value."""

        os = None
        with self.lock:
            self.check_disposed()
            if not self.is_stopped:
                os = self.observers[:]
                self.value = value
        if os:
            for o in os:
                o.on_next(value)

    def dispose(self):
        """Releases all resources used by the current instance of the
        ReplaySubject class and unsubscribe all observers."""

        with self.lock:
            self.is_disposed = True
            self.observers = None
            self.value = None
            self.exception = None



