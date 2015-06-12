from twisted.trial import unittest
from twutils import eventservice
from twisted.internet.task import Clock
import pythonioc

class Callback(object):
    calledWith = None
    def callback(self, arg):
        if arg == 'explode':
            raise Exception('this should not happen')
        self.calledWith = arg
    
globalCallbackValue = None
        
def globalCallback(arg):
    global globalCallbackValue
    globalCallbackValue = arg
    
class TestEventService(unittest.TestCase):
    
    clock = pythonioc.Inject('reactor')
        
    def setUp(self):    
        pythonioc.cleanServiceRegistry()
        pythonioc.registerServiceInstance(Clock(), 'reactor', True)
        self.events = eventservice.EventService()
        # reset the global value
        globalCallback(None)
        
    def test_weakCallback_boundmethod(self):
        cb = Callback()
        cb.callback('hello')
        self.assertEquals('hello', cb.calledWith)
        
        self.events.subscribeEvent('event', cb.callback)
        
        self.assertEquals(0, len(self.clock.getDelayedCalls()))
        self.events.triggerEvent('event', 'someparam')
        self.assertEquals(1, len(self.clock.getDelayedCalls()))
        
        self.clock.advance(1)
        self.assertEquals('someparam', cb.calledWith)
        
        # now we delete the callback
        del cb
        
        # triggering an event with 'explode' would raise an exception
        # if the callback would be called, but the event trigger
        # should ignore it.
        self.events.triggerEvent('event', 'explode')
        
        # rather check whether something is in the queue.
        self.clock.advance(1)

    def test_weakCallback_unboundmethod(self):
        
        self.events.subscribeEvent('event', globalCallback)
        self.assertEquals(None, globalCallbackValue)
        
        self.assertEquals(0, len(self.clock.getDelayedCalls()))
        self.events.triggerEvent('event', 'someparam')
        self.assertEquals(1, len(self.clock.getDelayedCalls()))
        self.clock.advance(1)
        self.assertEquals('someparam', globalCallbackValue)
        
    def test_unsubscribeEvent(self):
        # subscribe it, test it
        self.events.subscribeEvent('event', globalCallback)
        self.events.triggerEvent('event', 'value')
        self.assertEquals(1, len(self.clock.getDelayedCalls()))
        self.clock.advance(1)
        self.assertEquals('value', globalCallbackValue)
        
        # unsusbscribe it, trigger it, test again
        self.events.unsubscribeEvent('event', globalCallback)
        self.events.triggerEvent('event', 'value2')
        # no handler registered, no call delayed
        self.assertEquals(0, len(self.clock.getDelayedCalls()))
        self.assertEquals('value', globalCallbackValue)


    def test_subscribeUnsubscribeUniversal(self):
        """
        Checks subscribing and unsubscribing to global events.
        """
        self.events.subscribeUniversal(globalCallback)
        self.events.triggerEvent('someevent')
        self.assertEquals(1, len(self.clock.getDelayedCalls()))
        self.clock.advance(1)
        self.assertEquals('someevent', globalCallbackValue)
        
        # reset the variable
        globalCallback(None)
        
        self.events.unsubscribeUniversal(globalCallback)
        self.events.triggerEvent('someevent')
        self.assertEquals(0, len(self.clock.getDelayedCalls()))
        self.assertIsNone(globalCallbackValue)