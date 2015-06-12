from twisted.python import log, threadable



import random
import time
from twisted.internet import defer, task, threads
import traceback
import sys
from functools import wraps

__version__ = "0.1.1"


class _SafeFunctionRunner(object):
    def __init__(self, function, *args, **kwargs):
        self.func = function
        self.args = args
        self.kwargs = kwargs
        
        self.job = None
        self.maxfails = None
        self.fails = 0
        
        # time in milliseconds the task
        # needs to be running before
        # the looper prints its time
        self._minLogTime = 50
        
        self._running = 0
        
        self._allowOverlap = True
    
    @defer.inlineCallbacks
    def __call__(self):
        try:
            if self._running > 0 and not self._allowOverlap:
                log.msg('Looper %s is not allowed to overlap. Ignoring this round.' % (self.name,))
                return
                
            self._running += 1
            start = time.time()
            result = yield self.func(*self.args, **self.kwargs)
            self.fails = 0
            defer.returnValue(result)
        except Exception as e:
            _exc_type, _exc_value, exc_traceback = sys.exc_info()
            tb = traceback.extract_tb(exc_traceback)
            exc_location = traceback.format_list(tb[-3:])
            log.msg('Exception occured running LoopingCall %s: %s\n(%s)' % (self.name, str(e), exc_location))
            self.fails += 1
        finally:
            looperTime = round((time.time() - start) * 1000, 2)
            self._running -= 1
            if looperTime > self._minLogTime:
                log.msg('Looping call %s took %f ms' % (self.name, looperTime))
                
            if self.maxfails and self.fails >= self.maxfails:
                log.msg("Looper failed too many times (max %s). I'm giving up" % self.maxfails)
                self.job.stop()
            

    def setMinLogTime(self, minLogTime):
        self._minLogTime = minLogTime
        
    @property
    def name(self):
        return self.func.__name__
    
    def setMaxFails(self, job, maxfails):
        """
        Specify max number of fails along with the job that needs to be 
        stopped when the max fails are reached.
        """
        assert job, "Need job to stop when max fails reached"
        assert maxfails > 0, "maxfails needs to be > 0"
        self.maxfails = maxfails
        self.job = job
        
    def setOverlap(self, overlap):
        assert overlap in[False, True]
        self._allowOverlap = overlap
        
class _JitteredLoopingCall(task.LoopingCall):
    """
    Looping call that adds some jittering to the interval, thus avoiding to 
    load the reactor more balanced.
    """
    
    _rand = random.Random(time.time())
    
    def start(self, interval, now=True, jitter=0.083, maxfails=None, minLogTime=None, allowOverlap=True):
        realInterval = self._rand.normalvariate(interval,
                                              interval * jitter)
        
        if maxfails:
            self.f.setMaxFails(self, maxfails)
            
        if minLogTime:
            self.f.setMinLogTime(minLogTime)
            
        self.f.setOverlap(allowOverlap)
            
        return task.LoopingCall.start(self, realInterval, now)
    
    def stop(self, ignoreErrors=True):
        assert self.running or ignoreErrors, "Tried to stop non-running looper"
                    
        if self.running:
            task.LoopingCall.stop(self)
        
def deferredSleep(reactor, duration):
    """
    Delays execution using deferreds. Mostly used in inline-callbacks.
    Idea taken from
    http://comments.gmane.org/gmane.comp.python.twisted/19394
    
    Use it like
    @defer.inlineCallbacks
    def foo():
        yield doSomething()
        # this will wait for 3 seconds without blocking anything
        yield testutils.deferredSleep(3)
        yield doSomethingAfterwards()
        
    """
    d = defer.Deferred()
    reactor.callLater(duration, d.callback, None)
    return d
    

def createLoopingCall(reactor, function, *args, **kwargs):
    """
    Creates a looping call
    """
    looper = _JitteredLoopingCall(_SafeFunctionRunner(function, *args, **kwargs))
    looper.clock = reactor
    
    return looper

class _OneShotFunctionRunner(_SafeFunctionRunner):
    
    @defer.inlineCallbacks        
    def __call__(self):
        yield _SafeFunctionRunner.__call__(self)
        if self.fails == 0 and self.job.running:
            self.job.stop()

def startRetryingOneshotJob(reactor, function, args=(), kwargs={}, maxRetries=32, tryInterval=3.2):
    """
    Creates a oneshot job that executes once and tries maxRetries in case
    it crashes. After first successful execution it is being stopped.
    
    Best to use named parameters only!
    """
    
    looper = _JitteredLoopingCall(_OneShotFunctionRunner(function, *args, **kwargs))
    looper.clock = reactor
    looper.start(interval=tryInterval,
                 now=False,
                 maxfails=maxRetries,
                 allowOverlap=False)  # the oneshop job should not overlap!
    
    return looper

def runAsDeferredThread(func):
    """
    Decorates a function to run as a deferred thread when invoked in the reactor thread
    or reuse the same thread when invoked in a deferred thread already.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if isReactorThread():
            # print "creating new thread"
            return threads.deferToThread(func, *args, **kwargs)
        else:
            # print "run it directly"
            result = func(*args, **kwargs)
            assert not isinstance(result, defer.Deferred), "The inner function must be a deferred!"
            return result
    return wrapper


def isReactorThread():
    return threadable.isInIOThread()