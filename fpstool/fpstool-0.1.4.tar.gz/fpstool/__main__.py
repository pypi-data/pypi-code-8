# coding: utf-8

from . import *

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
        print 'Recv fps:', n

    recvfps(printer)

    raw_input()
    stop()
