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
    def __init__(self,dburl,limit):
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
    
    def pushData(self, data):
        self.collectedData.append(data)
        self.totalcount += 1
        if len(self.collectedData) >= self.limit:
            #print( "saving ...." )
            p = mp.Process(target=self.db.update, args=(self.collectedData,))
            self.jobs.append(p)
            p.start()
            #bulkUpload(self.db, self.collectedData)
            self.collectedData = []
            self.threadcount = len( [y for y in self.jobs if y.is_alive() == True] ) 
            print( "current threadcount: ", self.threadcount , "    ", "pushed documents: ", self.limit, "    ", "total docs so far: ", self.totalcount)
        return len(self.collectedData)
    
    def finish(self):
        for proc in self.jobs:
            print("waiting for upload-process " + str(proc) + " to finish ...")
            proc.join()
            del proc
        
        print("uploading final set of documents ...")
        self.db.update(self.collectedData)
        message = len(self.collectedData)
        self.collectedData = []
        return message
        
    def destroyDatabase(self):
        self.server.delete(self.dbname)
