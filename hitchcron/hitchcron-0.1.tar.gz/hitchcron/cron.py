import argparse
import time
import subprocess
from sys import argv, stdout, stderr, exit


def run():
    if len(argv) < 3:
        stderr.write("Usage: wait cmd ....\n")
        stderr.write("E.g. : 0.5 echo output something ....\n")
        stderr.flush()
        exit(1)

    try:
        float(argv[1])
    except ValueError:
        stderr.write("First argument must be a float, e.g. 1 or 0.5.\n")
        stderr.flush()
        exit(1)

    stdout.write("READY\n")
    stdout.flush()

    try:
        while True:
            #stdout.write(" ".join(argv[2:]))
            subprocess.call(argv[2:])
            time.sleep(float(argv[1]))
    except (KeyboardInterrupt, SystemExit):
        exit(0)

if __name__=='__main__':
    run()
