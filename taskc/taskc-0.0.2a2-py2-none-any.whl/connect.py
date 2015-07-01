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
        m = transaction.mk_message(org="Public",user="jack",key="07751281-b3d4-4d59-9f4d-ffdeb92b7135")
        m['type'] = "sync"
        final = transaction.prep_message(m)
        self.transport.write(final)


def got_protocol(p):
    print "has protocol"
    p.sendMessage()

    reactor.callLater(1, p.sendMessage, "This is sent in a second")
    reactor.callLater(2, p.transport.loseConnection)

# point = SSL4ClientEndpoint(reactor, "172.17.0.51", 53589, ContextFactory())
# d = connectProtocol(point, TaskClient())
# d.addCallback(got_protocol)
# reactor.run()

from twisted.internet import ssl, task, protocol, endpoints, defer
from twisted.python.modules import getModule

@defer.inlineCallbacks
def main(reactor):
    factory = protocol.Factory.forProtocol(TaskClient)
    certData = getModule(__name__).filePath.sibling('client.cert.pem').getContent()
    authData = getModule(__name__).filePath.sibling('client.key.pem').getContent()
    print authData
    clientCertificate = ssl.PrivateCertificate.loadPEM(authData)
    authority = ssl.Certificate.loadPEM(certData)
    # with open("/home/jack/.task/docker/client.key.pem") as f:
    #     data = f.read()
    #     print data
    #     clientCertificate = ssl.PrivateCertificate.loadPEM(data)
    # with open("/home/jack/.task/docker/client.cert.pem") as f:
    #     data = f.read()
    #     print data
    #     authority = ssl.Certificate.loadPEM(data)

    options = ssl.optionsForClientTLS(u'172.17.0.51', authority, clientCertificate)
    endpoint = endpoints.SSL4ClientEndpoint(reactor, '172.17.0.51', 53589, options)
    echoClient = yield endpoint.connect(factory)

    done = defer.Deferred()
    echoClient.connectionLost = lambda reason: done.callback(None)
    yield done

if __name__ == '__main__':
    import connect
    task.react(connect.main)