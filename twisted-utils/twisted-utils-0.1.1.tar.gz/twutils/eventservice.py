'''

@author: eh14
'''
import weakref
import collections
import pythonioc

#
# taken from http://code.activestate.com/recipes/578298-bound-method-weakref/
#
class _BoundMethodWeakref:
    def __init__(self, func):
        self.func_name = func.__name__
        self.wref = weakref.ref(func.__self__)  # __self__ returns the class http://docs.python.org/reference/datamodel.html

    def __call__(self):
        func_cls = self.wref()
        if func_cls is None:  # lost reference
            return None
        else:
            func = getattr(func_cls, self.func_name)
            return func

def weak_ref(callback):
    if hasattr(callback, '__self__') and callback.__self__ is not None:  # is a bound method?
        return _BoundMethodWeakref(callback)
    else:
        return weakref.ref(callback)
    

class EventService(object):
    """
    Simple registry object allowing to register and subscribe to events.
    Fireing an event results in new events being published to the event
    reactor queue.
    """
    
    _reactor = pythonioc.Inject('reactor')
    def __init__(self):
    
        self._events = collections.defaultdict(list)
        
        self._universalHandlers = []
    def triggerEvent(self, name, *args, **kwargs):
        for handler in self._events[name]:
            if handler():
                self._reactor.callLater(0, handler(), *args, **kwargs)
                
        # call universal handlers
        for handler in self._universalHandlers:
            if handler():
                self._reactor.callLater(0, handler(), name, *args, **kwargs)
                
    def subscribeEvent(self, name, function):
        ref = weak_ref(function)
        self._events[name].append(ref)
        
        self._cleanDeadHandlers()
        
        return ref
        
    def unsubscribeEvent(self, name, function):
        if name not in self._events:
            raise AttributeError('No event subscription for %s' % name)
        for handler in list(self._events[name]):
            if handler() == function:
                self._events[name].remove(handler)
                
        self._cleanDeadHandlers()
    
    def subscribeUniversal(self, function):
        """
        Subscribes to all events.
        Note that universal handlers get the first event name passed as first argument.
        """
        ref = weak_ref(function)
        self._universalHandlers.append(ref)
        self._cleanDeadHandlers()
        
        return ref
        
    def unsubscribeUniversal(self, function):
        for handler in list(self._universalHandlers):
            if handler() == function:
                self._universalHandlers.remove(handler)
                
        self._cleanDeadHandlers()
                
    def _cleanDeadHandlers(self):
        """
        Cleans all dead handlers, i.e. removes weak references that are not 
        available anymore.
        """
        for name in self._events.iterkeys():
            self._events[name] = filter(lambda h: h() is not None, self._events[name])
        
        self._universalHandlers = filter(lambda h: h() is not None, self._universalHandlers)
            
