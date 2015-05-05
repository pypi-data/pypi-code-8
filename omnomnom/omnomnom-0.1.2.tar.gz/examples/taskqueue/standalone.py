from omnomnom.generics.taskqueue import client


def task():
    import time
    print "executing task"
    time.sleep(4)
    print "Done executuing"
    return "sth"


with client.OmnomnomClient(u'tcp://127.0.0.1:7105', standalone=True) as c:
    c.execute('examples.taskqueue.standalone.task')