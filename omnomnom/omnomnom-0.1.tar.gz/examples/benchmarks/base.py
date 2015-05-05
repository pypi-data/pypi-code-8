# Inspired by: https://github.com/walkr/nanoservice/tree/master/benchmarks

import time
from multiprocessing import Process

import nanomsg
from omnomnom.models import Executable
from omnomnom.generics.micro import Fruit


class MultiplyExecutable(Executable):

    def __call__(self, x, y, **kwargs):
        return x + y


class JsonTestService(Fruit):
    multiply = MultiplyExecutable()


class JsonPubTestService(Fruit):
    socket_type = nanomsg.PUB
    multiply = MultiplyExecutable()


class Benchmark(object):

    def __init__(self, name, service_class, message_num, address, task, client_class):
        self.name = name
        self.service_class = service_class
        self.client_class = client_class
        self.message_num = message_num
        self.address = address
        self.task = task

    def handle_service(self, service):
        service.handle()

    def handle_client(self, client, task, args):
        res = client.get(task, args=args)
        assert not res['error']

    def run(self):
        print('')
        print(self.name)
        print('Dealing with {0} messages'.format(self.message_num))
        print('-----------------------------')

        service_process = Process(
            target=self.start_service, args=(self.address, self.message_num)
        )
        service_process.start()
        time.sleep(0.1)

        with self.client_class(address=self.address) as client:
            self.execute_benchmark(client, self.message_num, self.task)

        time.sleep(0.2)
        service_process.terminate()

    def execute_benchmark(self, client, message_num, task):

        pairs = [
            (x, x+1) for x in range(message_num)
        ]

        started = time.time()
        for pair in pairs:
            self.handle_client(client, task, pair)
        duration = time.time() - started
        print('Client stats:')
        self.print_stats(message_num, duration)

    def start_service(self, address, n):
        service = self.service_class(address=address)
        started = time.time()

        for _ in range(n):
            self.handle_service(service)

        duration = time.time() - started

        time.sleep(0.1)
        print('Service stats:')
        self.print_stats(n, duration)
        return

    def print_stats(self, n, duration):
        pairs = [
            ('Total messages', n),
            ('Total duration (s)', duration),
            ('Throughput (msg/s)', n/duration)
        ]
        for pair in pairs:
            label, value = pair
            print(' * {:<25}: {:10,.2f}'.format(label, value))


class RawBenchmark(Benchmark):

    def handle_service(self, service):
        data = service.socket.recv()
        service.socket.send(data)

    def handle_client(self, client, task, args):
        request = 'data'
        client.socket.send(request)
        response = client.socket.recv()
        assert request == response