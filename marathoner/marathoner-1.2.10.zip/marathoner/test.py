'''
In a case of a failure, this module tests various parts of Marathoner and outputs
the debug information.
'''
from os import path
import socket
import subprocess
import sys

from six import print_

from marathoner import MARATHONER_PORT
from marathoner.utils.ossignal import get_signal_name
from marathoner.utils.proc import start_process


class Test(object):
    def run(self):
        self.test_environment()
        self.test_mediator()

    def test_environment(self):
        print_('Running on platform', sys.platform, 'with python', sys.version)
        print_('Testing python version:')
        self._run_process(['python', '-V'])
        print_('Testing java version:')
        self._run_process(['java', '-version'])

    def test_mediator(self):
        mediator = __import__('marathoner.mediator', fromlist=['mediator']).__file__
        mediator = path.splitext(mediator)[0] + '.py'
        print_('Mediator location:', mediator)

        print_('Openning socket communication...')
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.bind(('127.0.0.1', MARATHONER_PORT))
            sock.listen(1)

            print_('Running mediator:')
            proc = start_process(['python', mediator])
            while proc.poll() is None:
                try:
                    conn, addr = self.sock.accept()
                except socket.timeout:
                    pass
                else:
                    conn.settimeout(None)
                    break
            else:
                code = proc.poll()
                print_('WARNING: Mediator ended with non-zero code:', get_signal_name(code))
                return
            print_('Connection accepted.')

            print_('Creating socket reader/writer')
            socket_reader = conn.makefile('rb')
            socket_writer = conn.makefile('wb')

            socket_reader.close()
            socket_writer.close()
        finally:
            sock.close()

    def _run_process(self, params):
        si = None
        if hasattr(subprocess, 'STARTUPINFO'):
            si = subprocess.STARTUPINFO()
            si.dwFlags = subprocess.STARTF_USESHOWWINDOW
            si.wShowWindow = subprocess.SW_HIDE
        return subprocess.Popen(
            params,
            shell=False,
            bufsize=1,
            universal_newlines=True,
            startupinfo=si).communicate()
