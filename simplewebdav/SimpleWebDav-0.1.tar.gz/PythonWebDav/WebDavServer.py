from PythonWebDav import Handler
import http.server
import sys


class WebDavServer:
    def __init__(self, path_to_folder, filer_class):
        self.handler = Handler.LHandler
        self.handler._filer = filer_class(path_to_folder)
        self.handler._XMLWorker._filer = filer_class(path_to_folder)

    def start(self, address, port):
        httpserver = http.server.HTTPServer((address, port), self.handler)
        print("Start at", port)
        httpserver.serve_forever()