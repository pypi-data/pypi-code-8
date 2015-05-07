# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

"""
Automated tests for Asset Cloud.

We dynamically `import *` for all modules inside this package,
which enables all our tests to get picked up.
"""

import os


basedir = os.path.dirname(__file__)

for root_dir, dirs, files in os.walk(basedir):
    relative_dir = root_dir[len(basedir):]
    package = __package__ + relative_dir.replace(os.path.sep, '.')
    components = [os.path.splitext(filename) for filename in files]
    modules = [basename for basename, ext in components
               if ext == '.py' and basename != '__init__']

    for module in modules:
        exec('from %s.%s import *' % (package, module))
