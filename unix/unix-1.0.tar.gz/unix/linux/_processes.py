import unix

class Processes(unix._processes.Processes):
    def __init__(self, host):
        unix._Processes.__init__(self, host)

    def list(self):
        return self._host.execute('ps', 'aux')
