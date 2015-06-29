#!/usr/bin/env python

import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom
import argparse
from os.path import exists

def set_node(node, paths, value=None, **kwargs):
    for n in paths:
        actual = [child for child in node.getchildren() if child.tag == n]
        node = actual[-1] if actual else ET.SubElement(node, n)
    if isinstance(value, dict):
        for key, value in kwargs.iteritems():
            ET.SubElement(node, key).text = value
    else:
        node.text = value

def change_node(filename, path, value):
    if exists(filename):
        tree = ET.parse(filename)
        root = tree.getroot()
        firstnode = path.split('/')[0]
        if firstnode != root.tag:
            raise Exception('invalid root node')
    else:
        root = ET.Element('config')

    paths = path.split('/')[1:]
    set_node(root, paths, value)

    tree = ET.ElementTree(root)
    xml = ET.tostring(root)
    # pretty = minidom.parseString(xml)
    # output = pretty.toprettyxml(indent="  ", newl="\n")
    with open(filename, 'w') as f:
        f.write(xml)

def main(argv):
    parser = argparse.ArgumentParser(
            prog = 'xmlconfig',
            description ='fix your xml config files'
        )

    parser.add_argument('input', metavar='INPUT', help="input xml file")
    parser.add_argument('path', metavar='PATH', help="xml node path (not xpath)")
    parser.add_argument('value', metavar='VALUE', help="new value")
    parser.set_defaults(func=set_node)

    args = parser.parse_args(argv)
    change_node(args.input, args.path, args.value)

if __name__ == '__main__':
    main(sys.argv[1:])
