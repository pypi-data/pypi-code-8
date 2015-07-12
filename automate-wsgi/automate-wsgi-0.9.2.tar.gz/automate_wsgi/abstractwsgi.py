# -*- coding: utf-8 -*-
# (c) 2015 Tuomas Airaksinen
#
# This file is part of automate-wsgi.
#
# automate-wsgi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# automate-wsgi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with automate-wsgi.  If not, see <http://www.gnu.org/licenses/>.

import threading
import socket

import tornado
import tornado.wsgi
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket

from traits.api import Instance, Int, CStr, Dict, Str

from automate.common import threaded
from automate.service import AbstractUserService


class TornadoService(AbstractUserService):

    """
    Abstract service that provides HTTP server for WSGI applications.
    """

    #: Which ip address to listen. Use ``0.0.0.0`` (default) to listen to all local networking interfaces.
    http_ipaddr = CStr("0.0.0.0")

    #: HTTP (or HTTPS if using SSL) port to listen
    http_port = Int(3000)

    #: Path to ssl certificate file. If set, SSL will be used.
    #:
    #: .. tip::
    #:
    #:   You may use script scripts/generate_selfsigned_certificate.sh to generate a
    #:   self-signed openssl certificate.
    ssl_certificate = CStr

    #: Path to ssl private key file
    ssl_private_key = CStr

    #: Number of listener threads to spawn
    num_threads = Int(5)

    #: Extra static dirs you want to serve. Example::
    #:
    #:    static_dirs = {'/my_static/(.*)': '/path/to/my_static'}
    static_dirs = Dict(key_trait=Str, value_trait=Str)

    _server = Instance(tornado.ioloop.IOLoop)
    _web_thread = Instance(threading.Thread)

    @property
    def is_alive(self):
        return self._web_thread and self._web_thread.is_alive()

    def get_wsgi_application(self):
        """
            Get WSGI function. Implement this in subclasses.
        """
        raise NotImplementedError

    def get_websocket(self):
        return None

    def get_filehandler_class(self):
        return tornado.web.StaticFileHandler

    def get_tornado_handlers(self):
        tornado_handlers = []
        websocket = self.get_websocket()
        if websocket:
            tornado_handlers.append(('/socket', websocket))

        for entrypoint, path in self.static_dirs.iteritems():
            tornado_handlers.append((entrypoint, self.get_filehandler_class(), {'path': path}))

        wsgi_app = self.get_wsgi_application()

        if wsgi_app:
            wsgi_container = tornado.wsgi.WSGIContainer(wsgi_app)
            tornado_handlers.append(('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_container)))
        return tornado_handlers

    def setup(self):
        tornado_app = tornado.web.Application(self.get_tornado_handlers())

        if self.ssl_certificate and self.ssl_private_key:
            ssl_options = {
                "certfile": self.ssl_certificate,
                "keyfile": self.ssl_private_key,
            }
        else:
            ssl_options = None

        server = tornado.httpserver.HTTPServer(tornado_app, ssl_options=ssl_options)

        try:
            server.listen(self.http_port, self.http_ipaddr)
        except socket.error as e:
            self.logger.error('Could not start server: %s', e)

        self._server = tornado.ioloop.IOLoop.instance()
        if not self._server._running:
            self._web_thread = threading.Thread(target=threaded(self._server.start),
                                                name="%s::%s" % (self.system.name, self.__class__.__name__))

            self._web_thread.start()
        else:
            self.logger.debug('Tornado IOLoop already running, no need to start new')

    def cleanup(self):
        if self.is_alive:
            self._server.stop()
