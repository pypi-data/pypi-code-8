class Disks(object):
    def __init__(self, host):
        self._host = host

    def list(self):
        pass
#        command = 'lsblk -io KNAME,TYPE,SIZE,MODEL --pairs | grep disk'
#        status, stdout, stderr = self._host.execute(command)
#        if not status:
#            raise LinuxError('unable to list disks: %s' % stderr)
#        return {name: {'size': size, 'model': model}
#                for line in stdout.splitlines()
#                for name, _, size, model in [[elt.split('=')[1][1:-1]
#                                              for elt in line.split()]]}
