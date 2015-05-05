import logging

from omnomnom.models import Executable
from omnomnom.generics.micro import Fruit


class PingExecutable(Executable):

    def __call__(self, *args, **kwargs):
        return 'pong'


class PongExecutable(Executable):

    def __call__(self, *args, **kwargs):
        return 'ping'


class ExceptionExecutable(Executable):

    def __call__(self, *args, **kwargs):
        raise Exception(u"Kaboom")


class LongExecutable(Executable):

    def __call__(self, *args, **kwargs):
        import time
        delta = int(kwargs['delta'])
        logging.info(u"Sleeping for {0} second(s)".format(delta))
        time.sleep(delta)
        return 'done'


class HeavyExecutable(Executable):

    def __call__(self, *args, **kwargs):
        import urllib2
        data = urllib2.urlopen('http://www.google.pl').read()
        # replaces invalid utf-8 characters
        return data.decode('utf-8', 'replace')


class PingPongService(Fruit):
    ping = PingExecutable()
    pong = PongExecutable()
    long = LongExecutable()
    heavy = HeavyExecutable()
    exc = ExceptionExecutable()


if __name__ == '__main__':
    service = PingPongService(address='tcp://127.0.0.1:5001', log_level='DEBUG')
    service.run()