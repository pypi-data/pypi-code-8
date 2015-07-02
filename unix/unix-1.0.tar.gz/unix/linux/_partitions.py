class Partitions(object):
    def __init__(self, host):
        self._host = host

    def list(self, dev='/dev/sda'):
        command = ('parted', dev, 'print')
        kwargs = dict(script=True, machine=True)
        status, stdout, stderr = self._host.execute(*command, **kwargs)
        if not status:
            raise LinuxError('unable to list partitions: %s' % stderr)

        partitions = {}
        for partition in stdout.splitlines()[2:]:
            number, start, end, _, _, desc, flags = partition.split(':')
            device = '%s%d' % (dev, number)
            partitions[device] = dict(start=start,
                                      end=end,
                                      desc=desc,
                                      flags=flags)
