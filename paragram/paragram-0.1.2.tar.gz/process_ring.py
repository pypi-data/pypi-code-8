#!/usr/bin/env python

import paragram as pg
import time

#import logging
#logging.basicConfig(level=logging.DEBUG)
#import multiprocessing; multiprocessing.util.log_to_stderr()
max = 16
start = time.time()

def offset():
	return time.time()

class link(object):
	def __init__(self, proc, id):
		print "%0.3f: process %s running..." % (offset(), id,)

		@proc.receive('spawn', pg.Process)
		def spawn(msg, first):
			if id < max:
				self.next = proc.spawn(link, name="link-%s" % (id+1,), args=(id+1,))
				self.next.send('spawn', first)
			else:
				print "completing the loop"
				self.first = first
				first.send('complete')

		@proc.receive('end')
		def end(msg):
			print "%.3f: process %s ending..." % (offset(), id,)
			if id == max:
				self.first.send('all_gone')
			else:
				self.next.send('end')
			proc.terminate()


def main():
	proc = None
	@pg.main.receive('complete')
	def up(*a):
		print "%.3f: all processes are running" %(offset(),)
		proc.send('end')

	@pg.main.receive('all_gone')
	def complete(*a):
		print "%.3f: all processes shut down" % (offset(),)
		pg.main.terminate()
	proc = pg.main.spawn(link, args=(0,), name="root")
	proc.send('spawn', pg.main)

def use_threads():
	global max, pg
	pg.default_type = pg.ThreadProcess
	max = 2000

#use_threads()
main()

# --------------------------------------
def main_threads():
	import time
	import Queue
	import multiprocessing
	manager = multiprocessing.Manager()
	q = manager.Queue()

	def thread_run():
		print "putting"
		q.put("hello there")
		time.sleep(5)

	import threading
	for i in xrange(0, 1000):
		print "spawning"
		thread = threading.Thread(target=thread_run)
		thread.daemon = True
		thread.start()
	print "waiting"
	
	try:
		while True:
			print q.get(False, timeout=1)
	except Queue.Empty: pass
	print "done"
#main_threads()


