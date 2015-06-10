from PythonWebDav import Filer,  AudioFiler
import urllib
import xml.etree.ElementTree as ET
import sys

"""
class 'Worker' provides functions for work with xml data
"""


class Worker(object):

    def call(self, request, prop, path):
        try:
            metname = 'do_' + request[6:].replace('-', '_')
            method = getattr(self, metname)
            self.path = path
            method(prop)
            self.path = None
        except:
            print(request[6:].replace('-', '_'))

    def create_xml(self, data, root, path):
        prop = self.create_response(root, path)
        for child in data:
            self.call(child.tag, prop, path)

    def create_xml_for_child(self, data, root, path):
        if self._filer.isdir(path):
            for file in self._filer.childs(path):
                self.create_xml(data, root, path+file)

    def parse_path(self, head):
        # print(urllib.parse.unquote(head))
        return urllib.parse.unquote(head)

    def root_response(self):
        """return root"""
        root = ET.Element("D:multistatus", {'xmlns:D': 'DAV:'})
        return root

    def create_response(self, root, url):
        response = ET.SubElement(root, "D:response")
        href = ET.SubElement(response, "D:href")
        href.text = url
        propstat = ET.SubElement(response, "D:propstat")
        prop = ET.SubElement(propstat, "D:prop")
        status = ET.SubElement(propstat, "D:status")
        status.text = "HTTP/1.1 200 OK"
        return prop

    def do_resourcetype(self, prop):
        if self._filer.isdir(self.path):
            restype = ET.SubElement(prop, "D:resourcetype")
            collect = ET.SubElement(restype, "D:collection")

    def do_creationdate(self, prop):
        date = ET.SubElement(prop, "D:creationdate")
        date.text = self._filer.get_creationdate(self.path)

    def do_displayname(self, prop):
        name = ET.SubElement(prop, "D:displayname")
        name.text = self._filer.get_name(self.path)

    def do_getcontentlength(self, prop):
        length = ET.SubElement(prop, "D:getcontentlength")
        length.text = self._filer.get_size(self.path)

    def do_getcontenttype(self, prop):
        type = ET.SubElement(prop, "D:getcontenttype")
        type.text = self._filer.get_mimetype(self.path)

    def do_getetag(self, prop):
        if not self._filer.isdir(self.path):
            etag = ET.SubElement(prop, "D:getetag")
            etag.text = self._filer.get_hash(self.path)

    def do_getlastmodified(self, prop):
        date = ET.SubElement(prop, "D:getlastmodified")
        date.text = self._filer.get_lastmodified(self.path)

    def do_quota_available_bytes(self, prop):
        bytes = ET.SubElement(prop, "D:quota-available-bytes")
        bytes.text = self._filer.get_freesize(self.path)

    def do_quota_used_bytes(self, prop):
        bytes = ET.SubElement(prop, "D:quota-used-bytes")
        bytes.text = self._filer.get_size(self.path)