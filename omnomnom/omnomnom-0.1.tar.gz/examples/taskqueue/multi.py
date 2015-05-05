from omnomnom.generics.taskqueue import client


def task():
    import time
    print "executing task"
    time.sleep(5)
    print "Done executuing"
    return "sth"


workers = [
    u'tcp://127.0.0.1:7105',
    u'tcp://127.0.0.1:7106'
]

with client.LycheeClient(workers, standalone=True, propagate_exc=True) as c:
    c.execute('examples.taskqueue.multi.task')