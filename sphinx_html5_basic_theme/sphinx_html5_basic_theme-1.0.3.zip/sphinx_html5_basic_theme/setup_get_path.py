# This file is called from the Sphinx every time
# we want to build domuments with the Sphinx,
# ONLY WHEN this package are installed into Python
# system(site-packages) with the pip or something
# similar tool.

from os import path
package_dir = path.dirname(path.abspath(__file__))

def get_path():
    return package_dir
