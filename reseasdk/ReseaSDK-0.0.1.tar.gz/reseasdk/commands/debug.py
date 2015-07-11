import os
import argparse
from reseasdk import info
from reseasdk.commands.build import build, load_packages, \
    load_current_package_yml


def main(args_):
    parser = argparse.ArgumentParser(prog='resea debug',
                                     description='debug an executable')
    parser.add_argument('-r', action='store_true', help='rebuild the executable')
    args = parser.parse_args(args_)

    target = 'test'
    build(target, args.r)

    config,_,_ = load_packages(load_current_package_yml(), target)
    cmd = config['HAL_DEBUG']
    path = 'build/{}/executable'.format(target)
    info('build has been successful, starting the executable with debugger...')
    os.execv(cmd, [cmd, path])
