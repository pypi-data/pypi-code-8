###############################################################
# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
#  Copyright (c) 2015, alelec
#  https://www.alelec.net
#
#  ls_json traverses either the provided path or current dir
#  and returns the file tree (with file sizes) in json format
#
# ls_json is free software; you can redistribute it and/or modify
# it under the terms of the PSF License as published by
# the Python Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# ls_json is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the PSF License
# along with ls_json.  If not, see <https://docs.python.org/2/license.html>

import os
import errno
from collections import defaultdict

def tree(): return defaultdict(tree)

def json_tree(path):
    all = tree()
    for root, dirs, files in os.walk(path):
        for f in files:
            rel_root = os.path.relpath(root, path)
            rel_dirs = rel_root.split(os.sep)
            entry = all if rel_root == '.' else all["."]
            for d in rel_dirs:
                entry = entry[d]
            entry[f] = os.path.getsize(os.path.join(root, f))
    return all["."]

def main():
    import json
    import sys

    try:
        directory = sys.argv[1]
    except IndexError:
        directory = "."

    print(json.dumps(json_tree(directory), indent=2, sort_keys=True))

if __name__ == '__main__':
    main()