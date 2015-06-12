import multiprocessing
import pickle
import traceback


class A(object):
    def hello(a):
        def f(x):
            return 2*x
        r = f(a)
        print r
        return r


def _producer():
    a=A()
    try:
        pickle.dumps(a.hello)
        q.put(a.hello)
    except Exception as e:
        print 'Pickling error : %s' % e
        traceback.print_exc()
        pass
    for i in range(5):
        q.put(i)
    q.put(None)

def _consumer():
    d = 0
    while d is not None:
        d = q.get()
        print d


q = multiprocessing.Queue()
p1 = multiprocessing.Process(target=_producer)
p2 = multiprocessing.Process(target=_consumer)


p1.start()
p2.start()

p1.join()
p2.join()