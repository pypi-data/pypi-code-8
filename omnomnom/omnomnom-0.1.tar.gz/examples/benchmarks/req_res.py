from omnomnom.models import Executable
from omnomnom.generics.micro import marshalling
from omnomnom.generics.micro import Fruit
from omnomnom.generics.micro import MicroClient

import base


class MultiplyExecutable(Executable):

    def __call__(self, x, y, **kwargs):
        return x + y


class JsonTestService(Fruit):
    marshaller = marshalling.JsonMarshaller()
    multiply = MultiplyExecutable()


class BsonTestService(Fruit):
    marshaller = marshalling.BsonMarshaller()
    multiply = MultiplyExecutable()


class MsgPackTestService(Fruit):
    marshaller = marshalling.MsgPackMarshaller()
    multiply = MultiplyExecutable()


class JsonClient(MicroClient):
    marshaller = marshalling.JsonMarshaller()


class BsonClient(MicroClient):
    marshaller = marshalling.BsonMarshaller()


class MsgPackClient(MicroClient):
    marshaller = marshalling.MsgPackMarshaller()


if __name__ == '__main__':
    message_num = 20000

    benchmark = base.Benchmark(
        name='Json Marshaller Req-Rep over IPC', service_class=JsonTestService,
        message_num=message_num, address='ipc:///tmp/bench-req-rep-ipc.sock',
        task='multiply', client_class=JsonClient
    )
    benchmark.run()

    benchmark = base.Benchmark(
        name='Json Marshaller Req-Rep over TCP', service_class=JsonTestService,
        message_num=message_num, address='tcp://127.0.0.1:5051',
        task='multiply', client_class=JsonClient
    )
    benchmark.run()

    benchmark = base.Benchmark(
        name='Bson Marshaller Req-Rep over IPC', service_class=BsonTestService,
        message_num=message_num, address='ipc:///tmp/bench-req-rep-ipc.sock',
        task='multiply', client_class=BsonClient
    )
    benchmark.run()

    benchmark = base.Benchmark(
        name='Bson Marshaller Req-Rep over TCP', service_class=BsonTestService,
        message_num=message_num, address='tcp://127.0.0.1:5051',
        task='multiply', client_class=BsonClient
    )
    benchmark.run()

    benchmark = base.Benchmark(
        name='Msgpack Marshaller Req-Rep over IPC', service_class=MsgPackTestService,
        message_num=message_num, address='ipc:///tmp/bench-req-rep-ipc.sock',
        task='multiply', client_class=MsgPackClient
    )
    benchmark.run()

    benchmark = base.Benchmark(
        name='Msgpack Marshaller Req-Rep over TCP', service_class=MsgPackTestService,
        message_num=message_num, address='tcp://127.0.0.1:5051',
        task='multiply', client_class=MsgPackClient
    )
    benchmark.run()

    message_num = 50000

    benchmark = base.RawBenchmark(
        name='RAW Req-Rep over IPC', service_class=JsonTestService,
        message_num=message_num, address='ipc:///tmp/bench-req-rep-ipc.sock',
        task='multiply', client_class=MicroClient
    )
    benchmark.run()

    benchmark = base.RawBenchmark(
        name='RAW Req-Rep over TCP', service_class=JsonTestService,
        message_num=message_num, address='tcp://127.0.0.1:5051',
        task='multiply', client_class=MicroClient
    )
    benchmark.run()

