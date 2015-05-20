from twisted.internet import reactor
from txsh import ls


def test(x):
    print 'STATUS CODE', x.status
    print 'OUTPUT', x.stdout
    print 'ERR Output', x.stderr
    reactor.stop()

# l = ls.bake("-l")
# d = ls("/")
# d = workon()
d = ls("-l", _out="test.txt")
# d = deactivate()
d.addCallback(test)
reactor.run()