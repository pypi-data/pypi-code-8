from datetime import timedelta
from time import time
import os


class Stats():
	def __init__(self):
		self.peak_clients = 0
		self.start_time = None
		self.current_clients = 0
		self.peak_fds = 0
		self.open_fds = 0
		self.avg_client_lifetime = None


	def update_clients(self, count):
		if self.peak_clients < count:
			self.peak_clients = count
		self.current_clients = count


	def update_open_fds(self):
		open_fds = 0
		'''with command('ls /proc/%d/fd | wc -l'%os.getpid()) as cmd:
			out, r = cmd.execute()
			if r == 0:
				open_fds = int(out)
			else:
				log.error('unable to obtain open fd count')
				return'''

		if open_fds > self.peak_fds:
			self.peak_fds = open_fds
		self.open_fds = open_fds


	def update_client_lifetime(self, lifetime):
		if self.avg_client_lifetime is None:
			self.avg_client_lifetime = lifetime
		else:
			self.avg_client_lifetime = (self.avg_client_lifetime + lifetime) / 2


	def __repr__(self):
		repr = ''
		repr += 'peak clients: %d\n'%self.peak_clients
		repr += 'live clients: %d\n'%self.current_clients
		repr += 'peak fds: %d\n'%self.peak_fds
		repr += 'open fds: %d\n'%self.open_fds
		repr += 'avg client life: '
		if self.avg_client_lifetime is None:
			repr += 'n.a.\n'
		else:
			repr += '%.2fs\n'%self.avg_client_lifetime
		repr += 'uptime: %s\n'%(str(timedelta(seconds=(int(time() - self.start_time)))))

		return repr

