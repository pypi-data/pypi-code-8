import argparse
import datetime
import os
import subprocess
from reseasdk import info
from reseasdk.commands.build import build


def main(args_):
    parser = argparse.ArgumentParser(prog='resea test',
                                     description='test an executable')
    parser.add_argument('-r', action='store_true', help='rebuild the executable')
    args = parser.parse_args(args_)

    build('test', args.r)
    info('build has been successful, starting the executable...')

    with open('build/test/boot.log', 'a') as f:
        f.write('================ {} ================\n'.format(
                str(datetime.datetime.now())))

    cmd = './build/test/executable 2>&1 |tee -a build/test/boot.log'
    subprocess.call(cmd, shell=True)
