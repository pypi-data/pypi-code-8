#!/usr/bin/env python
import os
import sys
from distutils.sysconfig import get_python_lib

def get_locally_installed_packages():
    path = get_python_lib()
    packages = {}
    for root, dirs, files in os.walk(path):
        for item in files:
            if "top_level" in item:
                with open(os.path.join(root, item), "r") as f:
                    package = root.split("/")[-1].split("-")
                    package_import = f.read().strip().split("\n")
                    for item in package_import:
                        if item not in ["tests", "_tests"]:
                            if len(package) < 2:
                                continue
                            packages[item] = {
                                'version': package[1].replace(".dist", ""),
                                'name': package[0]
                            }
    return packages

def get_pkg_names_from_import_names():
    result = []
    with open(os.path.join(os.path.dirname(__file__), "mapping"), "r") as f:
        return [x.strip().split(":")[0] for x in f.readlines()]

if __name__ == '__main__':
    packages = get_locally_installed_packages()
    mappings = get_pkg_names_from_import_names()
    for key, val in packages.iteritems():
        if key in mappings:
            continue
        if key.lower() != val['name'].lower() and "." not in val['name'] \
        and "_" not in key \
        and "jmbo" not in val['name'] \
        and "/" not in key \
        and len(key) > 3 and 'django' not in val['name']:
            print (key + ":" + val['name'])