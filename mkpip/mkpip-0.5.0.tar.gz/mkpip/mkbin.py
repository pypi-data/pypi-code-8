#!/usr/bin/env python
import os
from subprocess import check_output
IMPORTS_STANDARD = [
    'import os',
    'import sys',
]
IMPORTS_REQUESTS = [
    'import requests',
]
IMPORTS_SUBPROCESS = [
    'from subprocess import call, check_output, PIPE, Popen, CalledProcessError',
]
IMPORTS_COLLECTIONS = [
    'from collections import namedtuple',
    'from collections import defaultdict',
]
IMPORTS_BOTO = [
    'from boto import connect_s3',
    'from boto import connect_ec2',
    'from boto import connect_sqs',
]
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'templates', 'bin.py')

def render(imp_standard=True, imp_subprocess=False, imp_collections=False,
        imp_requests=False, imp_boto=False, flags=None, opts=None, pos=None):
    with open(TEMPLATE_PATH) as f:
        temp = f.read()
    imports = []
    if imp_standard:
        imports += IMPORTS_STANDARD
    if imp_subprocess:
        imports += IMPORTS_SUBPROCESS
    if imp_collections:
        imports += IMPORTS_COLLECTIONS
    if imp_requests:
        imports += IMPORTS_REQUESTS
    if imp_boto:
        imports += IMPORTS_BOTO
    imports = '\n'.join(imports)
    args = []
    if flags is not None:
        for flag in flags.split(','):
            args += [
                "parser.add_argument('--{}', '-{}', action='store_true')".format(
                flag.lower(), flag[0])
            ]
    if opts is not None:
        for o in opts.split(','):
            opt, default = o.split('=')
            if default.isdigit():
                args += [
                    "parser.add_argument('--{}', '-{}', type=int, default={})".format(
                        opt.lower(), opt[0], default
                    )
                ]
            elif default.lower() in ('none', 'null'):
                args += [
                    "parser.add_argument('--{}', '-{}')".format(
                        opt.lower(), opt[0]
                    )
                ]
            else:
                args += [
                    "parser.add_argument('--{}', '-{}', default='{}')".format(
                        opt.lower(), opt[0], default
                    )
                ]
    if pos is not None:
        for p in pos.split(','):
            args += ["parser.add_argument('{}')".format(p)]
    if args:
        args = ['    '+arg for arg in args]
        args = '\n'.join(args)
    else:
        args = ''
    temp = temp.format(imports=imports, args=args)
    return temp

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', '-o', default='bin.py', help='script path')
    parser.add_argument('--standard', '-s', action='store_true',
        help='add os,sys imports')
    parser.add_argument('--subprocess', '-S', action='store_true',
        help='add subprocess imports')
    parser.add_argument('--collections', '-c', action='store_true',
        help='add collections, namedtuple and defaultdict')
    parser.add_argument('--requests', '-r', action='store_true',
        help='add requests import statement')
    parser.add_argument('--boto', '-b', action='store_true',
        help='add boto connection import statements')
    parser.add_argument('--flags', '-f', help='name of flags')
    parser.add_argument('--pos', '-p', help='name of positionals')
    parser.add_argument('--opts', '-O', help='name of optionals')
    args = parser.parse_args()
    
    template = render(imp_standard=args.standard, 
        imp_subprocess=args.subprocess,
        imp_collections=args.collections,
        imp_requests=args.requests,
        imp_boto=args.boto,
        flags=args.flags,
        pos=args.pos,
        opts=args.opts,
    )
    with open(args.output, 'w') as f:
        f.write(template)
    print('Wrote to {}'.format(args.output))

if __name__ == '__main__':
    main()
