"""The following is borrowed heavily from Products.CMFSquidTool. That code
is ZPL licensed.

Asynchronous purging works as follows:

* Each remote host gets a queue and a worker thread.

* Each worker thread manages its own connection.  The queue is not processed
  until it can establish a connection.  Once a connection is established, the
  queue is purged one item at a time. Should the connection fail, the worker
  thread again waits until a connection can be re-established.
"""

import atexit
import logging
import Queue
import threading
import requests
import json

from App.config import getConfiguration
from zope.interface import implements

from plone.cachepurging.interfaces import IPurger

logger = logging.getLogger('wildcard.cloudflare')


class CloudflarePurgerFactory(object):

    implements(IPurger)

    def __init__(self, backlog=200):
        self.queue = Queue.Queue(backlog)
        self.worker = Worker(self.queue, self)
        self.backlog = backlog
        self.queueLock = threading.Lock()

    def purgeAsync(self, urls, zone_id, api_key, email):
        if not self.worker.isAlive():
            self.worker.start()
        try:
            self.queue.put((urls, zone_id, api_key, email), block=False)
            logger.debug('Queued %s' % ','.join(urls))
        except Queue.Full:
            # Make a loud noise. Ideally the queue size would be
            # user-configurable - but the more likely case is that the purge
            # host is down.
            if not getConfiguration().debug_mode:
                logger.warning("The purge queue for the URL %s is full - the "
                               "request will be discarded.  Please check the "
                               "server is reachable, or disable this purge "
                               "host", ','.join(urls))

    def purgeSync(self, urls, zone_id, api_key, email):
        headers = {
            'X-Auth-Email': email,
            "X-Auth-Key": api_key,
            'Content-Type': 'application/json'
        }
        resp = requests.delete(
            'https://api.cloudflare.com/client/v4/zones/%s/purge_cache' % zone_id,
            headers=headers, data=json.dumps({'files': urls}))
        logger.debug('Finished purge for %s' % ','.join(urls))
        return resp

    def stopThreads(self, wait=False):
        self.worker.stopping = True
        try:
            self.queue.put(None, block=False)
        except Queue.Full:
            # no problem - self.stopping should be seen.
            pass
        ok = True
        if wait:
            self.worker.join(5)
            if self.worker.isAlive():
                logger.warning("Cloudflare worker thread failed to terminate")
                ok = False
        return ok


class Worker(threading.Thread):
    """Worker thread for purging.
    """

    def __init__(self, queue, producer):
        self.producer = producer
        self.queue = queue
        self.stopping = False
        super(Worker, self).__init__(name="PurgeThread for cloudflare")

    def stop(self):
        self.stopping = True

    def run(self):
        logger.debug("%s starting", self)
        # Queue should always exist!
        q = self.producer.queue
        atexit.register(self.stop)
        try:
            while not self.stopping:
                item = q.get()
                if self.stopping or item is None:  # Shut down thread signal
                    logger.debug('Stopping worker thread for '
                                 '(%s, %s).' % (self.host, self.scheme))
                    break
                urls, zone_id, api_key, email = item

                try:
                    self.producer.purgeSync(urls, zone_id, api_key, email)
                    # XXX check valid response
                except Exception:
                    logger.exception('Failed to purge %s', ','.join(urls))
        except:
            logger.exception('Exception in worker thread '
                             'for (%s, %s)' % (self.host, self.scheme))
        logger.debug("%s terminating", self)

CloudflarePurger = CloudflarePurgerFactory()


def stopThreads():
    purger = CloudflarePurger
    purger.stopThreads()

from zope.testing.cleanup import addCleanUp
addCleanUp(stopThreads)
del addCleanUp
