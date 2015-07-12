import os
import yaml
import psutil
from sup.mailer import Mailer


register_path = '/tmp/yama'
config_path = os.path.expanduser('~/.yama')
conf = yaml.load(open(config_path, 'r'))


def pid():
    """
    Convenience func for getting the current script's pid.
    """
    return os.getpid()


def register(pid):
    """
    Register a new process by id.
    """
    p = psutil.Process(pid)
    pname = ' '.join(p.cmdline())
    with open(register_path, 'a') as f:
        f.write('{}:{}\n'.format(pid, pname))


def deregister(pid):
    """
    Degister a process by id.
    """
    ps = []
    with open(register_path, 'r') as f:
        for l in f.readlines():
            ps.append(_parse_register_line(l))

    with open(register_path, 'w') as f:
        for pid_, pname_ in ps:
            if pid_ != pid:
                f.write('{}:\n'.format(pid_, pname_))


def audit():
    """
    Check that registered processes are still running.
    """
    if not os.path.exists(register_path):
        return

    expected_ps = []
    with open(register_path, 'r') as f:
        for l in f.readlines():
            expected_ps.append(_parse_register_line(l))

    expected_pids = [pid for pid, pname in expected_ps]
    running_pids = psutil.pids()

    missing_pids = set(expected_pids) - set(running_pids)
    if not missing_pids:
        return

    m = Mailer(**conf['mailer'])
    missing_ps = [(pid, pname) for pid, pname in expected_ps if pid in missing_pids]
    for pid, pname in missing_ps:
        subject = 'Missing: {}'.format(pname)
        body = 'Process [{}] ({}) was expected to be running, but was not found'.format(pname, pid)
        m.notify(subject, body, conf['mailer']['admins'])
        deregister(pid)


def _parse_register_line(line):
    parts = line.split(':')
    pid = int(parts[0])
    pname = ':'.join(parts[1:]).strip()
    return pid, pname