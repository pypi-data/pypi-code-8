from PythonWebDav import XmlWorker, Filer, AudioFiler
import http.server
import xml.etree.ElementTree as ET
import sys


class LHandler(http.server.BaseHTTPRequestHandler):
    _XMLWorker = XmlWorker.Worker()
    # _filer = AudioFiler.AudioFiler(PATH_TO_FILE)

    def send_msg(self, s):
        self.wfile.write(bytes(s, "utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Allow', 'OPTIONS, GET, HEAD, POST, PUT, DELETE, COPY, MOVE, MKCOL, PROPFIND')
        self.send_header('Allow', 'PROPPATCH')
        self.send_header('DAV', '1, 2')
        self.end_headers()
        return

    def do_PROPFIND(self):
        length = int(self.headers['Content-Length'])
        request_xml = self.rfile.read(length).decode('utf-8')
        path = self._XMLWorker.parse_path(self.path)
        depth = int(self.headers['Depth'])
        if length == 0:
            request_xml = '<?xml version="1.0" encoding="utf-8" ?>\
             <D:propfind xmlns:D="DAV:">\
              <D:prop>\
            <D:resourcetype/>\
              </D:prop>\
             </D:propfind>'
        xml_data = ET.fromstring(request_xml)

        root = self._XMLWorker.root_response()

        self._XMLWorker.create_xml(xml_data[0], root, path)

        if depth == 1:
            self._XMLWorker.create_xml_for_child(xml_data[0], root, path)

        a = str(ET.tostring(root), encoding='utf-8')

        self.responses[207] = ('Multi-Status', 'Multiple responses')
        self.send_response(207, message='Multi-Status')
        self.send_header("Content-type", 'text/xml; encoding="utf-8"')
        self.send_header("Content-Length", str(len(a)))
        self.end_headers()
        self.send_msg(a)

    def do_GET(self):
        path = self._XMLWorker.parse_path(self.path)
        try:
            with self._filer.get_file(path) as file:
                self.send_response(200)
                self.send_header("Content-type", self._filer.get_mimetype(path))
                self.end_headers()
                self.wfile.write(file.read())
        except FileNotFoundError:
            print("File ", path, " not found")
            self.send_response(404, message='Not found')
            self.end_headers()

    def do_MKCOL(self):
        path = self._XMLWorker.parse_path(self.path)
        self._filer.create_folder(path)
        self.send_response(201, message='Created')
        self.end_headers()

    def do_DELETE(self):
        path = self._XMLWorker.parse_path(self.path)
        self._filer.delete(path)
        self.send_response(204, message='No Content')
        self.end_headers()

    def do_PUT(self):
        path = self._XMLWorker.parse_path(self.path)
        length = int(self.headers['Content-Length'])
        self._filer.create_file(path, self.rfile, length)
        self.send_response(201, message='Created')
        self.end_headers()

    def do_MOVE(self):
        path_from = self._XMLWorker.parse_path(self.path)
        host = self.headers['Host']
        location = self.headers['Destination'].replace("http://", "").replace(host, "")
        path_to = self._XMLWorker.parse_path(location)
        overwrite = self.headers['Overwrite']
        self._filer.move_file(path_from, path_to, overwrite)
        self.send_response(201, message='Created')
        self.send_header("Location:", location)
        self.end_headers()

    def do_COPY(self):
        path_from = self._XMLWorker.parse_path(self.path)
        host = self.headers['Host']
        path_to = self._XMLWorker.parse_path(self.headers['Destination'].replace("http://", "").replace(host, ""))
        overwrite = self.headers['Overwrite']
        loc = self._filer.copy_file(path_from, path_to, overwrite)
        self.send_response(201, message='Created')
        self.send_header("Location:", loc)
        self.end_headers()

    def do_HEAD(self):
        pass