import random

from omnomnom.generics.micro import PubFruit


if __name__ == '__main__':
    address = 'tcp://127.0.0.1:5005'
    service = PubFruit(address=address, log_level='INFO')

    while True:
        response = service.marshaller.prepare_response(
            result=random.randint(1, 10000)
        )
        service.send_response(response)