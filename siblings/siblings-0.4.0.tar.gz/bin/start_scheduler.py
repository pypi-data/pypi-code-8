#!/usr/bin/env python

from __future__ import print_function, absolute_import
import configparser
import os
import sys
import argparse
import resource

import siblings.scheduler

dflt_cfg_path = '~/.config/siblings/config.cfg'
help_txt = {'config': "Path to config file. By default the config is read "
                      "from {}.".format(dflt_cfg_path),
            'verbose': "Increase verbosity of scheduler"}

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

    db = siblings.scheduler.Writer(cfg.get('SCHEDULER', 'db_path'), {})
    worker = siblings.scheduler.AllAllJobScheduler(db, dict(cfg.items('SCHEDULER')),
                                                   verbose=(options.verbose > 0))
    worker.start()



if __name__ == '__main__':
    main(sys.argv[1:])