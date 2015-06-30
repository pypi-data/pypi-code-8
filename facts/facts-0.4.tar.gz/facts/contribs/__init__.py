from contextlib import suppress
from facts import graft
from facts import serializer
import subprocess


@graft
def facter_info():
    """Returns data from facter.
    """

    with suppress(FileNotFoundError):  # facter may not be installed
        proc = subprocess.Popen(['facter', '--yaml'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        if not proc.returncode:
            data = serializer.load(stdout)
            return {'facter': data}
