from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.python import log
from twisted.internet.endpoints import SSL4ClientEndpoint, connectProtocol
from twisted.internet.ssl import ContextFactory


import transaction


# - Server address and port - TaskdConnection call
# - Organization name -
# - User name
# - Password [secret]
# - Certificate [secret]
# - Key [secret]

# class TaskdConnection(object):

#     def __init__(self, host, port=53589, **kwargs):
#         pass
#     def connect(self):
# do we need this?
# self.cadata = getcadata()
#         self.context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
#         self.connection =  context.wrap_socket(socket.socket(socket.AF_INET))
#         self.connection.connect(self.host, self.port)



class TaskClient(Protocol):
    def sendMessage(self):
        m = transaction.mk_message(org="public",user="jack",key="a69f8b68-5747-4ed3-af70-e891e9888fff")
        s = m.as_string()
        our_len = len(s) + 4
        
        self.transport.write("Hello")


def got_protocol(p):
    print "has protocol"
    p.sendMessage()
    reactor.callLater(1, p.sendMessage, "This is sent in a second")
    reactor.callLater(2, p.transport.loseConnection)

point = SSL4ClientEndpoint(reactor, "192.168.1.110", 53589, ContextFactory())
d = connectProtocol(point, TaskClient())
d.addCallback(got_protocol)
reactor.run()
