import xml.etree.ElementTree as ET
from lxml import etree

import logging
import os

class EpubParser(object):
    base = ''
    manifest = {}
    titles = {}
    spine = []
    spine_element_num = str(3) #replace this with xml check for which child of root 'spine' is x 2

    def __init__(self, path):
        self.name = path.replace('/', '')
        
        folder = path  + "/"
        if os.path.isdir(folder) == True:
            rootfile = self.parse_root_file(folder)
            if rootfile:
                self.rootfile = rootfile
                self.base = folder + os.path.dirname(rootfile)
                self.manifest = self.parse_manifest(folder + rootfile)
                self.tocPath = self.get_toc_path(self.manifest)

            if self.tocPath:
                self.toc = self.parse_toc(self.base + "/" + self.tocPath)

            self.spine = self.parse_spine(folder + rootfile)
        else :
            raise EpubError("No Rootfile found")

    def parse_root_file(self, folder):
        container = folder + "/META-INF/container.xml"

        if os.path.isfile(container):
            tree = ET.parse(container)
            root = tree.getroot()

            for rootfiles in root:
                for rf in rootfiles:
                    rootfile = rf.attrib['full-path']
                    return rootfile # Stop at first rootfile for now

        else:
            raise EpubError('No container.xml found')

        return False

    def parse_metadata(self, filename):
        raise NotImplementedError

    def parse_manifest(self, filename):
        """
        Parse the content.opf file.
        """
        namespaces = {'xmlns': 'http://www.idpf.org/2007/opf',
            'dc':'http://purl.org/dc/elements/1.1/',
            'dcterms':'http://purl.org/dc/terms/'}

        logging.debug("Parsing Manifest")

        items = {}

        # begin parsing content.opf
        tree = ET.parse(filename)
        root = tree.getroot()
        # extract item hrefs and place in return list
        for child in root.findall('xmlns:manifest/xmlns:item', namespaces=namespaces):
            item_id = child.attrib['id']

            if not item_id in items:
                items[item_id] = {}
                items[item_id]["href"] = child.attrib['href']
                items[item_id]["media-type"] = child.attrib['media-type']

        return items

    def get_toc_path(self, manifest):
        """
        From the manifest items, find the item for the Toc
        Return the Toc href
        """
        if "ncxtoc" in manifest:
            return manifest["ncxtoc"]["href"]
        else:
            for item in manifest.values():
                if item["media-type"] == "application/x-dtbncx+xml":
                    return item["href"]

        raise EpubError("No Toc File Found")

    def parse_toc(self, filename):
        namespaces = {'xmlns': 'http://www.daisy.org/z3986/2005/ncx/'}

        logging.debug("Parsing TOC")

        items = []

        # begin parsing content.opf
        #tree = ET.parse(filename)
        #root = tree.getroot()
        tree = etree.parse(filename)
        root = tree.getroot()

        # extract item hrefs and place in return list
        for nav_point in root.findall('xmlns:navMap/xmlns:navPoint', namespaces=namespaces):
            nav_label = nav_point.find('xmlns:navLabel', namespaces=namespaces)
            title = nav_label.getchildren()[0].text.encode("utf-8")
            href = nav_point.getchildren()[1].attrib['src'].encode("utf-8")
            item = {}

            item['id'] = nav_point.attrib['id']
            item['title'] = title
            self.titles[href] = title
            items.append(item)

        return items

    def parse_spine(self, filename):
        """
            Parse the content.opf file.
        """
        namespaces = {'xmlns': 'http://www.idpf.org/2007/opf',
                'dc':'http://purl.org/dc/elements/1.1/',
                'dcterms':'http://purl.org/dc/terms/'}

        logging.debug("Parsing Spine")

        spinePos = 1

        items = []

        # begin parsing content.opf
        tree = ET.parse(filename)
        root = tree.getroot()
        # extract item hrefs and place in return list
        for child in root.findall('xmlns:spine/xmlns:itemref', namespaces=namespaces):
            item = {}

            item["idref"] = child.attrib['idref']
            item["spinePos"] = spinePos

            item["cfiBase"] = "/" + "/".join([ self.spine_element_num, str(spinePos*2) + '[{}]'.format(item['idref']) ])

            if item["idref"] in self.manifest:
                item["href"] = self.manifest[item["idref"]]['href']

            # print self.titles
            if self.titles and item["href"] in self.titles:
                item['title'] = self.titles[item["href"]]
            else:
                item['title'] = ''

            items.append(item)

            spinePos += 1

        return items

class EpubError(Exception):
    pass
