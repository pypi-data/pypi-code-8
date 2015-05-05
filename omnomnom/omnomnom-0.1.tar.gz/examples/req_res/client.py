import random

from omnomnom.generics.micro import MicroClient


if __name__ == '__main__':
    with MicroClient(address='tcp://127.0.0.1:5001') as client:
        print client.get(executable='ping')
        print client.get(executable='pong')
        print client.get(executable='exc')
        print client.get(executable='heavy')
        print client.get(executable='long', kwargs={
            'delta': random.randint(1, 5)
        })