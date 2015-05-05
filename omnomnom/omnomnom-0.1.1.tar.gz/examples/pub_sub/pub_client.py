from omnomnom.generics.micro import MicroSubClient


if __name__ == '__main__':
    address = 'tcp://127.0.0.1:5005'
    total = 0
    with MicroSubClient(address=address) as client:
        for response in client.get_responses():
            total += 1
            if total % 10000 == 0:
                print "Client received {0} messages".format(total)