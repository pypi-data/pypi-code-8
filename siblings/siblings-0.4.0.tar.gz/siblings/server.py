import zmq
import threading
import jsonrpc2_zeromq as zmq_rpc
from .common import package_logger
from .db import Reader

class RPCWorkerServer(zmq_rpc.RPCServer):
    """Define a RPCServer which is connecting instead of binding to a socket.
    
    This is usally necessary if server is an instance of a worker behind a Dealer. 
    See ZeroMQ Guide for more details on this pattern."""
    def __init__(self, endpoint, context=None, timeout=1000, socket_type=None,
                     logger=None):
         super(zmq_rpc.RPCServer, self).__init__(endpoint, socket_type, timeout, context,
                                         logger=logger)
         self.socket = self.context.socket(self.socket_type)
         self.socket.connect(self.endpoint)
         self.poller = zmq.Poller()
         self.poller.register(self.socket, zmq.POLLIN)


class ReadAllAllMatchesHandler(RPCWorkerServer):
    """ a class to handle read requests for allall matches """
    def __init__(self, reader, endpoint, logger=None):
        super(ReadAllAllMatchesHandler,self).__init__(endpoint, logger=logger)
        if logger==None:
            self._logger=package_logger
        else:
            self._logger = logger
        self._reader = reader
        self._logger.info("Server started and listening on "+endpoint)

    def handle_getmatchesbetweengenomepair_method(self, genome1, genome2, **kw):
        return self._reader.get_matches_between_genomes(genome1, genome2)

    def handle_gethomologsofgene_method(self, genome, entry, **kw):
        return self._reader.get_homologs_of_gene(genome1, entry, **kw)
    

def start_service(filename, frontend_url, context=None, nr_workers=4, logger=None):
    """This function sets up a ZMQ Router/Dealer Proxy and starts 
    a set of worker threads which handle the read requests in parallel.
    
    Parameters:
     frontend_url: url to bind for the clients
     filename: the filename of the master pytables file.
     nr_workers: the number of worker threads started to serve data to the users
                 in parallel. Defaults to 4 threads. 
     logger: the logger used for the application. defaults to the package logger"""
    if context is None:
        context = zmq.Context.instance()
    if logger is None:
        logger = package_logger

    frontend = context.socket(zmq.ROUTER)
    frontend.bind(frontend_url)
    backend_url = 'inproc://workers'
    backend = context.socket(zmq.DEALER)
    backend.bind(backend_url)
    workers = []
    for i in range(nr_workers):
        dbHandler = Reader(filename)
        p = ReadAllAllMatchesHandler(dbHandler, endpoint=backend_url, logger=logger)
        p.start()
        workers.append(p)
    
    try:
        zmq.device(zmq.QUEUE, frontend, backend)
    except KeyboardInterrupt:
        for p in workers:
            p.stop()
    
    frontend.close()
    backend.close()
    context.term()


if __name__ == "__main__":
    start_service()
