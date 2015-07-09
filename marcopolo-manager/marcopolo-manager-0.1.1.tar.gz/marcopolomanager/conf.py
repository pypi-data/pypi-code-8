# -*- coding: utf-8 -*-
from os.path import dirname, join, isabs
import logging

from six.moves import configparser

CONF_DIR = '/etc/marcopolomanager'

RUNDIR = '/var/run/'
LOGDIR = '/var/log/marcopolo'

PIDFILE = 'marcopolomanagerd.pid'
LOGFILE = 'marcopolomanagerd.log'

DEBUG_LEVEL = 'DEBUG'

MANAGERS_DIR = '/etc/marcopolomanager/managers/'

default_values  = {
	'RUNDIR':RUNDIR,
	'LOGDIR':LOGDIR,
	'PIDFILE':PIDFILE,
	'LOGFILE':LOGFILE,
	'MANAGERS_DIR':MANAGERS_DIR,
}

config = configparser.RawConfigParser(default_values, allow_no_value=False)

DEPLOYER_FILE_READ = join(CONF_DIR, 'marcopolomanager.cfg')

try:
	with open(DEPLOYER_FILE_READ) as fp:
		config.readfp(fp)

		RUNDIR = config.get('marcopolomanager', 'RUNDIR')
		LOGDIR = config.get('marcopolomanager', 'LOGDIR')

		PIDFILE = config.get('marcopolomanager', 'PIDFILE')
		PIDFILE = PIDFILE if isabs(PIDFILE) else join(RUNDIR, PIDFILE)

		LOGFILE = config.get('marcopolomanager', 'LOGFILE')
		LOGFILE = LOGFILE if isabs(LOGFILE) else join(LOGDIR, LOGFILE)
		DEBUG_LEVEL = config.get('marcopolomanager', 'DEBUG_LEVEL').upper()
		MANAGERS_DIR = config.get('marcopolomanager', 'MANAGERS_DIR')
except IOError as i:
	logging.warning("Warning! The configuration file could not be read. Defaults will be used as fallback")
except Exception as e:
	logging.warning("Unknown exception in configuration parser %s" % e)