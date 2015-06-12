'''

@author: eh14
'''
from twisted.internet import selectreactor
from twisted.internet.base import DelayedCall
import time
import collections

# Global profiler variable, used by all 
_profiler = None
class Profiler(object):
    
    def __init__(self, outfile='profile.prof'):
        self._times = collections.defaultdict(list)
        self._outfile = outfile
    def addRecord(self, subject, duration):
        print type(subject), subject
        self._times[subject.__name__].append(duration)
        
        
    def dump(self, sort='cum'):
        """
        Dumps the results to a file.
        @param sort: sort by field. Default is cum.
        """
        
        fields = ['name', 'num', 'cum', 'avg']
        
        assert sort in fields, "invalid sort field"
        
        
        # create a list of tuples (name, num, cum, avg)
        grouped = []
        
        for func, records in self._times.iteritems():
            num = len(records)
            cum = sum(records)
            avg = cum / num
            name = str(func)
            grouped.append((name, num, cum, avg))
        
        sortIndex = fields.index(sort)
        grouped.sort(lambda l, r:cmp(r[sortIndex], l[sortIndex]))
        
        with open(self._outfile, 'w') as out:
            print >> out, ' '.join(fields)
            for record in grouped:
                print >> out, record[0], record[1], '%.4f' % (record[2] * 1000), '%.4f' % (record[3] * 1000)
        
class _ThreadCallQueueList(list):
    def append(self, element):
        f, args, kwargs = element
        list.append(self, (_ProfilingFunction(f), args, kwargs))
        
class _ProfilingFunction(object):
    def __init__(self, func):
        self.f = func
    
    def __getattr__(self, name):    
        return getattr(self.f, name)
    
    def __call__(self, *args, **kwargs):
        start = time.time()
        r = self.f(*args, **kwargs)
        _profiler.addRecord(self.f, time.time() - start)
        return r
    
    def __iter__(self):
        return iter(self.f)
    
class _ProfilingList(list):
    
    def append(self, element):
        if isinstance(element, DelayedCall):
            element.func = _ProfilingFunction(element.func)
        else:
            element = _ProfilingFunction(element)
        list.append(self, element)
    

def install():
    global _profiler
    selectreactor.install()
    
    _profiler = Profiler() 
    from twisted.internet import reactor
    reactor.threadCallQueue = _ThreadCallQueueList()
    reactor._pendingTimedCalls = _ProfilingList()
    reactor._newTimedCalls = _ProfilingList()
    reactor.addSystemEventTrigger('before', 'shutdown', _profiler.dump)  # @UndefinedVariable
    
