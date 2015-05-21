from __future__ import print_function, absolute_import
import unittest
from ..zmq import *
import time
import zmq


class EchoClient(MajorDomoClient):
    msgs = ['Hello World', "I'm a Unittest"]
    def run_device(self):
        reply = []
        for msg in self.msgs:
            self.send('echo', msg)
            reply.append(self.recv()[0])
        return reply


class EchoServer(ThreadMajorDomoWorker):
    def __init__(self, url, time_to_answer=0.001):
        super(EchoServer, self).__init__(url, 'echo', True)
        self.time_to_answer = time_to_answer

    def run_device(self):
        reply = None
        while True:
            reply = self.recv(reply)
            time.sleep(self.time_to_answer)

class EchoTest(unittest.TestCase):
    def setUp(self):
        url = 'tcp://127.0.0.1:9125'
        self.queue = ThreadMajorDomoBroker()
        self.queue.bind(url)
        self.client = EchoClient(url)
        self.worker = EchoServer(url)

    def test_echo_service(self):
        self.queue.start()
        self.worker.start()
        self.client.init_in_subprocess()
        res = self.client.run_device()
        self.assertEqual(self.client.msgs, res)


class SendOrReceiveOnceClient(MajorDomoClient):
    def __init__(self, url, identity, typ):
        super(SendOrReceiveOnceClient, self).__init__(url, verbose=True)
        self.setsockopt(zmq.IDENTITY, identity)
        self.typ = typ

    def run_device(self):
        if self.typ == 'send':
            self.send('echo', 'Hello World')
        elif self.typ == 'recv':
            self.timeout = 1000
            return self.recv()
        else:
            NotImplementedError('Typ unknown')

class ReconnectTest(unittest.TestCase):
    def setUp(self):
        self.url = "tcp://127.0.0.1:9125"
        self.queue = ThreadMajorDomoBroker(True)
        self.queue.bind(self.url)
        self.worker = EchoServer(self.url, time_to_answer=0.5)

    @unittest.skip(u"doesn't work properly yet. TODO: fix it!")
    def test_disconnect_and_new_client(self):
        client_identity = b'reconnecting'
        self.queue.start()
        self.worker.start()
        client1 = SendOrReceiveOnceClient(self.url, client_identity, 'send')
        client1.start()

        client2 = SendOrReceiveOnceClient(self.url, client_identity, 'recv')
        client2.init_in_subprocess()
        answer = client2.run_device()
        self.assertIsNotNone(answer, "Didn't receive any answer")
        self.assertEqual(answer[0], 'Hello World')

