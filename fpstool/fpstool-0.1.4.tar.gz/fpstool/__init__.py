# coding: utf-8
#
# Thanks to
# http://synack.me/blog/using-python-tcp-sockets

import os
import socket
import subprocess
import threading
import time
import requests


PORT = 7100
GOFPSPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fpstool')

def _adb(args, serialno=None):
    ''' Run adb comands '''
    output = subprocess.check_output(['adb'] + args)
    return output


def init():
    # Install gofps to phone
    _adb(['push', GOFPSPATH, '/data/local/tmp/'])
    _adb(['shell', 'chmod', '755', '/data/local/tmp/fpstool'])

    # Start fpstool
    _adb(['shell', '/data/local/tmp/fpstool', '-daemon'])

    # Forward port
    #_adb(['forward', '--remove-all']) # FIXME(ssx): maybe there is a better way.
    _adb(['forward', 'tcp:7100', 'tcp:57575'])
    wait()


def wait(timeout=12):
    for i in range(timeout):
        if timeout-i <= 10: print timeout-i
        try:
            r = requests.get('http://localhost:%d/api/version' % PORT, timeout=0.5)
            return True
        except:
            time.sleep(1.0)
    raise RuntimeError("connect to phone port error")

def stop():
    requests.get('http://localhost:%d/api/shutdown' % PORT)

def _readlines(sock, recv_buffer=4096, delim='\n'):
    buffer = ''
    data = True
    while data:
        data = sock.recv(recv_buffer)
        buffer += data

        while buffer.find(delim) != -1:
            line, buffer = buffer.split('\n', 1)
            yield line
    return


def recvfps(handler):
    sock = socket.socket()
    sock.connect(("localhost", PORT))
    sock.send("GET /hijack HTTP/1.1\r\n\r\n")
    #sock.send("Hello world\n")
    def receiver():
        for line in _readlines(sock):
            handler(float(line))
    th = threading.Thread(target=receiver)
    th.daemon = True
    th.start()

if __name__ == '__main__':
    init()

    import signal
    def handler(signum, frame):
        print 'Signal handler called with signal', signum
        stop()
        exit(0)

    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGQUIT, handler)

    def printer(n):
        print 'Recv:', n

    recvfps(printer)

    time.sleep(5.0)
