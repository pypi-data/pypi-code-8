#!/usr/bin/env python

from __future__ import print_function, absolute_import
import configparser
import os
import sys
import argparse
import resource

import siblings.aligner

dflt_cfg_path = '~/.config/siblings/config.cfg'
help_txt = {'config': "Path to config file. By default the config is read "
                      "from {}.".format(dflt_cfg_path)}

def main(args):
    parser = argparse.ArgumentParser("Start a siblings alignment worker job")
    parser.add_argument('-c', '--config', default=dflt_cfg_path, help=help_txt['config'])
    parser.add_argument('-v', '--verbose', action='count')

    options = parser.parse_args(args)
    try:
        cfg = configparser.ConfigParser()
        cfg.read(options.config)
    except configparser.ParsingError as e:
        sys.stderr.write(e)
        sys.exit(1)

    resource.setrlimit(resource.RLIMIT_STACK, (65532000, 65532000))
    worker = siblings.aligner.AlignWorker(dict(cfg.items('ALIGNER')))
    worker.start()



if __name__ == '__main__':
    main(sys.argv[1:])