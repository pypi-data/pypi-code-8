# -*- coding: utf-8 -*-
"""
couch-bulk-multiprocess

To upload a big amount of document to a CouchDB, it is recommended to use the
built-in bulk-upload functionality of CouchDB.
This module provides an async IO interface to store a stream of incoming
documents.
This is done by collecting the documents and push them as a bulk upload to the
database as soon as a given threshold is reached. By the use of threads these
uploads are performed in parallel und are performed while the original program
keeps on running.

Make sure to call mpcouchPusher.finish() at the end!
"""

import multiprocessing as mp
import couchdb


class mpcouchPusher():
    """A class that collects documents and uploads them as bulk as soon as a
    certain limit has been reached.

    Methods
    -------
    __init__(db,limit):
        Initializes the mpcouchPusher object.

        db: must be a valid CouchDB database object

        limit: specifies the amount of documents that need to be collected
               before they are pushed to the databases collectively.

    pushData(data):
        Stores the content of data to the databas specified at creation date.

        data: must be a valid CouchDB document in JSON format.

    finish:
        must be called after the last document has been pushed to the pushData
        function to ensure that all started processes finish and no data is
        lost.
    """
    def __init__(self, dburl, limit):
        self.collectedData = []
        self.dbname = "/".join(dburl.split("/")[-1:])
        self.dbhost = "/".join(dburl.split("/")[:-1])
        self.server = couchdb.Server(self.dbhost)
        try:
            self.db = self.server[self.dbname]
        except couchdb.ResourceNotFound:
            self.db = self.server.create(self.dbname)
        self.limit = limit
        self.totalcount = 0
        self.jobs = []
        self.threadcount = 0
        self.jobsbuffer = []
        self.jobslimit = 1
        self.finished = False

    def pushData(self, data):
        self.collectedData.append(data)
        self.totalcount += 1
        if len(self.collectedData) >= self.limit:
            # generate a new process and store in in the jobsbuffer
            p = mp.Process(target=self.db.update, args=(self.collectedData,))
            self.jobsbuffer.append(p)
            print("spawned process {}".format(len(self.jobs)+len(self.jobsbuffer)))
            self.collectedData = []
        self.threadcount = len([y for y in self.jobs if y.is_alive() is True]) # analysis:ignore
        if self.threadcount < self.jobslimit:
            # there is room for a new job, so take one from the jobsbuffer
            if len(self.jobsbuffer) > 0:
                newp = self.jobsbuffer.pop()
                self.jobs.append(newp)
                newp.start()
                self.threadcount = len([y for y in self.jobs if y.is_alive() is True]) # analysis:ignore
                print("processcount: {} process-queue: {}  collected so far: {}".format(self.threadcount, len(self.jobsbuffer), self.totalcount))
        return len(self.collectedData)

    def finish(self):
        waitForCompletion = True # for later implementation, not yet functional
        print("generate final upload process ...")
        if len(self.collectedData) > 0:
            p = mp.Process(target=self.db.update, args=(self.collectedData,))
            self.jobsbuffer.append(p)
        while len(self.jobsbuffer) > 0:
            # as long as there are still jobs in the queue, exectue them
            self.threadcount = len([y for y in self.jobs if y.is_alive() is True]) # analysis:ignore
            if self.threadcount < self.jobslimit:
                newp = self.jobsbuffer.pop()
                self.jobs.append(newp)
                newp.start()
                self.threadcount = len([y for y in self.jobs if y.is_alive() is True]) # analysis:ignore
                print("processcount: {} process-queue: {}  collected so far: {}".format(self.threadcount, len(self.jobsbuffer), self.totalcount))            

        # now, the jobsqueue is empty, we have to wait for the remaining jobs to complete
        if waitForCompletion == True:
            # but only, if we were told to do so by the argument "waitForCompletion"
            for proc in [runningJob for runningJob in self.jobs if runningJob.is_alive() is True]:
                print("waiting for upload-process {0} to finish ...".format(proc))
                proc.join()
                del proc
                self.finished = True
        else:
            # if we should not wait for it, just update the self.finished variable
            # this makes it possible for the parent app to check, whether it is save to quit already
            while len([runningJob for runningJob in self.jobs if runningJob.is_alive() is True]) > 0:
                self.finished = False
            self.finished = True
        for proc in self.jobs:
            del proc
        message = len(self.collectedData)
        self.collectedData = []
        return message

    def destroyDatabase(self):
        self.server.delete(self.dbname)
