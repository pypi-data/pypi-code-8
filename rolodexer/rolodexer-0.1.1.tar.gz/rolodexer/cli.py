#!/usr/bin/env python
"""
Usage:
  rolodexer INFILE [-o OUTFILE] [-V | --verbose]
  rolodexer -h | --help | -v | --version
    
Options:
  -o OUTFILE --output=OUTFILE       specify output file [default: stdout]
  -V --verbose                      print verbose output
  -h --help                         show this text
  -v --version                      print version

"""

from __future__ import print_function
# from os.path import join, dirname
from os.path import exists, isdir, dirname
from docopt import docopt
import parser as rolodexer
import json
import sys

JSON_ARGS = dict(indent=2, sort_keys=True)

def cli(argv=None):
    if not argv:
        argv = sys.argv
    
    arguments = docopt(__doc__, argv=argv[1:],
                                help=True,
                                version='0.1.0')
    
    # print(argv)
    # print(arguments)
    # sys.exit()
    
    entries = []
    errors  = []
    ipth = arguments.get('INFILE')
    opth = arguments.get('--output')
    
    with open(ipth, 'rb') as fh:
        idx = 0
        while True:
            linen = fh.readline()
            if not linen:
                break
            line = linen.strip()
            tokens = rolodexer.tokenize(line)
            try:
                terms = rolodexer.classify(tokens)
            except rolodexer.RolodexerError:
                errors.append(idx)
            else:
                entries.append(terms)
            idx += 1
        
        output_dict = { u"entries": entries, u"errors": errors }
        
        if opth == 'stdout':
            output_json = json.dumps(output_dict, **JSON_ARGS)
            print(output_json, file=sys.stdout)
        elif not exists(opth) and isdir(dirname(opth)):
            with open(opth, 'wb') as fp:
                json.dump(output_dict, fp, **JSON_ARGS)

if __name__ == '__main__':
    cli(sys.argv)