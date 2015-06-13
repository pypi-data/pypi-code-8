"""piston3

Just a wrapper for piston/

- For `import piston3` locally from repo.
- To keep original piston/ src dir.
- setup.py installs piston/ as piston3.

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
from path import path as Path

__path__ = [Path(__path__[0]).dirname().abspath() / 'piston']
