# -*- coding: utf-8 -*-
"""
A simple module to do repetitive tasks in the morning. 

Targeted as updating git repos.

"""

__author__ = 'Matthias Bussonnier'
__email__ = 'bussonniermatthias@gmail.com'
__version__ = '0.1.3'

version = __version__

import sys
import os
import re
from os.path import expanduser
import configparser
import io
import argparse

import logging
log = logging.getLogger(__file__)
console=log

logging.root.setLevel(logging.INFO)
logging.root.addHandler(logging.StreamHandler())

class _config(object):

    def __enter__(self):
        self.config = configparser.ConfigParser()
        self.config.read(expanduser('~/.morning'))

        return self.config

    def __exit__(self, *args_):
        with io.open(expanduser('~/.morning'),'w') as f:
            self.config.write(f)
        



def main():

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='subcommands', dest='subcmd')
    parser_add = subparsers.add_parser('add',help='')
    parser_status = subparsers.add_parser('status',help='')
    parser_list = subparsers.add_parser('list',help='')
    

    parser_add.add_argument('dir', nargs='*', default=('.',))

    args = parser.parse_args()

    if args.subcmd == 'add':
        for dr in args.dir:
            directory = os.path.abspath(expanduser(dr))
            if not os.path.isdir(directory):
                log.warn('%s is not a directory'%directory)
                continue
            if not os.path.isdir(os.path.join(directory,'.git')):
                log.warn('%s is not a git directory'%directory)
                continue
            log.info('adding %s to list of git repos to update'%str(directory))
            with _config() as config:
                if not 'mornings' in config.sections():
                    config['mornings'] = {}
                config['mornings'][directory] = 'true'

    elif args.subcmd == 'list':
        with _config() as config:
            for k in config['mornings'].keys():
                log.info(k)
                log.debug('%s' %(k))

    elif args.subcmd == 'status':
        status()
    else :
        status(gfo=True)
        log.info('no arguments, will update all the things.')

def status(gfo=False):
    from subprocess import Popen, run, DEVNULL, PIPE
    with _config() as config:
        for k in config['mornings'].keys():
            #log.info('will update git in {}'.format(k))
            fast_forward = False
            if gfo:
                res = run(['git','fetch','origin'],cwd=k, stdout=PIPE, stderr=PIPE)
                if res.returncode is not 0 :
                    log.error("could not fetch %s"%k)
                    continue
                c = configparser.ConfigParser()
                c.read(os.path.join(k,'.git/config'))
                fast_forward = (c.get('morning', 'fast-forward', fallback=None) == 'True')
                log.debug("configured for auto fast-forward %s" % fast_forward)
            res = run('git rev-parse --abbrev-ref HEAD'.split(), cwd=k, stdout=PIPE, stderr=PIPE)
            branch = res.stdout.decode().strip()
            res = run('git status -sb --porcelain'.split(), cwd=k, stdout=PIPE, stderr=PIPE)
            m = re.findall('behind ([0-9]+)', res.stdout.splitlines()[0].decode());
            behind = int(m[0]) if m else 0
            m = re.findall('ahead ([0-9]+)', res.stdout.splitlines()[0].decode());
            ahead = int(m[0]) if m else 0
            if behind and not ahead and branch == 'master':
                extra = 'can be fast-forwarded'
                if fast_forward: 
                    log.debug('is ffding')
                    res = run(['git','merge','origin/master','--ff-only'], cwd=k, stdout=PIPE, stderr=PIPE)
                    if res.returncode is not 0 :
                        log.error(res.stderr.decode())
                    extra = ' [fast-forwarded]'
            else:
                extra = ''

            log.info('{:50s} on branch {:7s} -{:02d},+{:02d}, {:s}'.format(k,branch, behind, ahead, extra))






if __name__ =='__main__':
    main()
