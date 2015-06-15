__author__ = 'Hi'
import os

import setuptools

def smart_find_packages(package_list):
    packages = []
    for pkg in package_list.strip().split("\n"):
        print "[FIND_PACKAGE] pkg: ", pkg
        pkg_path = pkg.replace('.', os.path.sep)
        print "[FIND_PACKAGE] pkg_path: ", pkg_path
        packages.append(pkg)
        print "[FIND_PACKAGE] packages.append(pkg): ", packages.append(pkg)
        packages.extend(['%s.%s' % (pkg, f) for f in setuptools.find_packages(pkg_path)])
        print "[FIND_PACKAGE] packages.extend(['%s.%s' % (pkg, f) for f in setuptools.find_packages(pkg_path)]): ", packages.extend(['%s.%s' % (pkg, f) for f in setuptools.find_packages(pkg_path)])
    return "\n".join(set(packages))
