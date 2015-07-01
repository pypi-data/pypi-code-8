import sys
import logging


class Logger():
	def __init__(self):
		self._log = logging.getLogger('mayloop')
		self._log.propagate = False
		self._to_stdout = False


	def start(self, logfile, loglevel=logging.ERROR):
		if logfile == 'stdout':
			logst = logging.StreamHandler(sys.stdout)
			logst.setLevel(loglevel)
			self._log.addHandler(logst)
			self._to_stdout = True
		else:
			logfh = logging.FileHandler(logfile)
			logfh.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
			logfh.setLevel(loglevel)
			self._log.addHandler(logfh)
			self._to_stdout = False
			
		self._log.setLevel(loglevel)

	
	def to_stdout(self):
		return self._to_stdout


	def debug(self, msg):
		self._log.debug(msg)


	def info(self, msg):
		self._log.info(msg)


	def warning(self, msg):
		self._log.warning(msg)


	def error(self, msg):
		self._log.error(msg)


log = Logger()
