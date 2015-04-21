"""
This file is part of dispy project.
See http://dispy.sourceforge.net for details.
"""

__author__ = "Giridhar Pemmasani (pgiri@yahoo.com)"
__email__ = "pgiri@yahoo.com"
__copyright__ = "Copyright 2015, Giridhar Pemmasani"
__contributors__ = []
__maintainer__ = "Giridhar Pemmasani (pgiri@yahoo.com)"
__license__ = "MIT"
__url__ = "http://dispy.sourceforge.net"

__all__ = ['Server']

import sys
import os
import threading
import json
import cgi
import time
import atexit
import traceback

if sys.version_info.major > 2:
    from http.server import BaseHTTPRequestHandler, HTTPServer
else:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import dispy
from dispy import DispyJob

class Server(object):
    class _HTTPRequestHandler(BaseHTTPRequestHandler):
        def __init__(self, ctx, DocumentRoot, *args):
            self._dispy_ctx = ctx
            self._dispy_ctx._http_handler = self
            self.DocumentRoot = DocumentRoot
            BaseHTTPRequestHandler.__init__(self, *args)

        def log_message(self, fmt, *args):
            dispy.logger.debug('HTTP client %s: %s' % (self.client_address[0], fmt % args))

        def do_GET(self):
            if self.path == '/updates':
                self._dispy_ctx._cluster_lock.acquire()
                nodes = self._dispy_ctx._cluster_updates.values()
                self._dispy_ctx._cluster_updates = {}
                self._dispy_ctx._cluster_lock.release()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                updates = {'jobs':{'submitted':self._dispy_ctx._jobs_submitted,
                                   'done':self._dispy_ctx._jobs_done},
                           'nodes':[node.__dict__ for node in nodes]}
                self.wfile.write(json.dumps(updates).encode())
                return
            elif self.path == '/status':
                self._dispy_ctx._cluster_lock.acquire()
                nodes = self._dispy_ctx._cluster_status.values()
                self._dispy_ctx._cluster_lock.release()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                updates = {'jobs':{'submitted':self._dispy_ctx._jobs_submitted,
                                   'done':self._dispy_ctx._jobs_done},
                           'nodes':[node.__dict__ for node in nodes]}
                self.wfile.write(json.dumps(updates).encode())
                return
            elif self.path == '/' or self.path == '/cluster.html':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                path = os.path.join(self.DocumentRoot, 'cluster.html')
                try:
                    f = open(path)
                    html = f.read()
                    self.wfile.write((html % {'TIMEOUT':str(self._dispy_ctx._poll_sec)}).encode())
                    f.close()
                    return
                except:
                    dispy.logger.warning('HTTP client %s: Could not read/send "%s"',
                                         self.client_address[0], path)
                    dispy.logger.debug(traceback.format_exc())
                self.send_error(404)
                return
            else:
                path = self.path[1:]
                try:
                    if path in ('jquery.js', 'cluster.css'):
                        f = open(os.path.join(self.DocumentRoot, path))
                        self.send_response(200)
                        self.send_header('Content-type',
                                         'text/javascript' if path.endswith('.js') else 'text/css')
                        self.end_headers()
                        self.wfile.write(f.read().encode())
                        f.close()
                        return
                except:
                    dispy.logger.warning('HTTP client %s: Could not read/send "%s"',
                                         self.client_address[0], path)
                    dispy.logger.debug(traceback.format_exc())
                self.send_error(400)
                return

        def do_POST(self):
            if self.path == '/timeout':
                form = cgi.FieldStorage(fp=self.rfile, headers=self.headers,
                                        environ={'REQUEST_METHOD':'POST'})
                for item in form.list:
                    if item.name != 'timeout':
                        continue
                    try:
                        timeout = int(item.value)
                    except:
                        dispy.logger.warning('HTTP client %s: invalid timeout "%s" ignored', 
                                             self.client_address[0], item.value)
                        timeout = 0
                    if timeout >= 1:
                        self._dispy_ctx._poll_sec = timeout
                        self.send_response(200)
                        return
            dispy.logger.warning('HTTP client %s: invalid POST request "%s" ignored', 
                                 self.client_address[0], self.path)
            self.send_response(400)
            return

    def __init__(self, host='', port=8181, poll_sec=10, DocumentRoot=None):
        if not DocumentRoot:
            DocumentRoot = os.path.join(os.path.dirname(__file__), 'data')
        self._cluster_status = {}
        # TODO: maintain updates for each client separately, so
        # multiple clients can view the status?
        self._cluster_updates = {}
        self._cluster_lock = threading.Lock()
        self._jobs_submitted = 0
        self._jobs_done = 0
        if poll_sec < 1:
            dispy.logger.warning('invalid poll_sec value %s; it must be at least 1' % poll_sec)
            poll_sec = 1
        self._poll_sec = poll_sec
        self._http_handler = None
        self._server = HTTPServer((host, port), lambda *args: \
                                  self.__class__._HTTPRequestHandler(self, DocumentRoot, *args))
        self._httpd_thread = threading.Thread(target=self._server.serve_forever)
        self._httpd_thread.daemon = True
        self._httpd_thread.start()

    def cluster_status(self, status, node, job):
        if status == DispyJob.Created:
            self._jobs_submitted += 1
            return
        if status == DispyJob.Finished or status == DispyJob.Terminated or \
               status == DispyJob.Cancelled or status == DispyJob.Abandoned:
            self._jobs_done += 1

        if node is not None:
            self._cluster_lock.acquire()
            self._cluster_status[node.ip_addr] = node
            self._cluster_updates[node.ip_addr] = node
            self._cluster_lock.release()

    def shutdown(self, wait=True):
        if wait:
            dispy.logger.debug(
                'HTTP server waiting for %s seconds for client updates before quitting',
                self._poll_sec)
            time.sleep(self._poll_sec)
        self._server.shutdown()

if __name__ == '__main__':
    # testing
    import logging
    server = Server(poll_sec=5)
    dispy.logger.setLevel(logging.DEBUG)
    while True:
        try:
            cmd = sys.stdin.readline().strip().lower()
            if cmd == 'quit' or cmd == 'exit':
                break
        except KeyboardInterrupt:
            break
    server.shutdown()
