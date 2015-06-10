from PythonWebDav import WebDavServer, Filer
import os

server = WebDavServer.WebDavServer(os.path.abspath(os.path.curdir), Filer.Filer)
server.start("0.0.0.0", 8080)