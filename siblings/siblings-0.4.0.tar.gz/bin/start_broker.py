#!/usr/bin/env python

from __future__ import print_function, absolute_import
import configparser
import sys
import argparse

import siblings.zmq

dflt_cfg_path = '~/.config/siblings/config.cfg'
help_txt = {'config': "Path to config file. By default the config is read "
                      "from {}.".format(dflt_cfg_path),
            'verbose': "Increase verbosity of worker"}

def main(args):
    parser = argparse.ArgumentParser("Start a siblings scheduler job")
    parser.add_argument('-c', '--config', default=dflt_cfg_path, help=help_txt['config'])
    parser.add_argument('-v', '--verbose', action='count', help=help_txt['verbose'])

    options = parser.parse_args(args)
    try:
        cfg = configparser.ConfigParser()
        cfg.read(options.config)
    except configparser.ParsingError as e:
        sys.stderr.write(e)
        sys.exit(1)

    port = cfg.getint('ALIGNER', 'queue_port')
    broker = siblings.zmq.MajorDomoBroker(options.verbose > 0)
    broker.bind('tcp://*:{}'.format(port))
    broker.start()



if __name__ == '__main__':
    main(sys.argv[1:])