from PythonWebDav import WebDavServer, Filer, AudioFiler

server = WebDavServer.WebDavServer("DavFolder", AudioFiler.AudioFiler)
server.start("0.0.0.0", 8080)