from multiprocessing.pool import ThreadPool, TimeoutError
from datetime import datetime

import socket
import logging
import time

try:
    import queue
except ImportError:
    import Queue as queue # Python 2 compat.

class WorkerManager(object):
    """ Manages all of the available daemon workers """

    def __init__(self, config, max_processes=5):
        self.workers = {}
        self.config = config
        self.pool = ThreadPool(processes=max_processes)

    def add(self, ident, func):
        """ Add a worker to the WorkerManager's control list.

        Args:
          ident (string): A unqiue identifier for the worker
          worker (WorkerThread): The worker thread to manage

        Returns:
          bool: The worker was added successfully.

        Raises:
          TypeError: If a non-WorkerThread type is provided in the 'worker' arg

        """

        self.logger = logging.getLogger('Manager')

        # If it's not already assigned, assign it.
        if(ident not in self.workers):
            self.workers[ident] = {
                'method': func,
                'pipe': self.pool.apply_async(func, []) # Start immediately
            }

    def get(self, ident):
        if ident not in self.workers:
            raise AttributeError("Thread with identifier '' not found".format(ident))

        return self.workers[ident]

    def collect_all(self):
        data = []

        # collect results
        for worker, result in self.workers.iteritems():
            tries = 0
            collected = None

            while tries < 5 and collected is None:
                try:
                    collected = result['pipe'].get(timeout=0)

                    for point in collected:
                        point['columns'].append('host')

                        # Append the hostname to each of the values.
                        for stat in point['points']:
                            stat.append(self.config.sysmond['hostname'])

                        # Add extra info
                        point['timestamp'] = time.time()

                    # Merge the lists
                    data += collected

                    # Start collection again
                    result['pipe'] = self.pool.apply_async(result['method'], [])
                except TimeoutError:
                    self.logger.warn("'{}' is taking too long to collect or something is wrong".format(
                        worker
                    ))

                    # Check if we've missed the limit
                    if (tries + 1) is 6:
                        self.logger.warn("Skipping collection of '{}'".format(worker))
                    else:
                        time.sleep(1)

                    tries += 1;

        return data

    def status(self):
        return self.workers
