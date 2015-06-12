'''

@author: eh14
'''
from twisted.web import server
from twisted.python import log


class LoggingSite(server.Site):
    def log(self, request):
        """
        Log a request's result to the logfile, by default in combined log format.
        """
        if request.uri.startswith('/static'):
            return
        
        line = '%s (%s) -> %s' % (self._escape(request.uri),
                                  self._escape(request.method),
                                  request.code)
        log.msg(line)
