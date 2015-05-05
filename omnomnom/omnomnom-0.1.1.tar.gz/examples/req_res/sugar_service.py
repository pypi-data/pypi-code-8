from omnomnom.models import Executable
from omnomnom.generics.micro import Fruit


service = Fruit(
    address='tcp://127.0.0.1:5001',
    log_level='DEBUG'
)


@service.to_registry(name='ping')
class PingExecutable(Executable):

    def __call__(self, *args, **kwargs):
        return 'pong'


@service.to_registry(name='pong')
class PongExecutable(Executable):

    def __call__(self, *args, **kwargs):
        return 'ping'


@service.to_registry(name='this_wont_be_registered')
class Dummy(object):
    pass


if __name__ == '__main__':
    service.register_executable(name='ddddd', executable=PingExecutable())
    service.run()