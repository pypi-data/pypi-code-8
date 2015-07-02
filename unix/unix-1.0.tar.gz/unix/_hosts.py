import re
FILE = '/etc/hosts'

class Hosts:
    def __init__(self, host):
        self._host = host


    def list(self):
        with self._host.open(FILE) as fhandler:
            return [(elt[0], tuple(elt[1:]))
                    for line in fhandler.read().splitlines()
                    if line and not line.decode().startswith('#')
                    for elt in [re.split('\t|\s+', line.decode())]]


    def add(self, ip, hosts):
        pass


    def delete(self, ip):
        pass


    def update(self, ip, hosts):
        pass


    def sync(self, elts):
        pass
