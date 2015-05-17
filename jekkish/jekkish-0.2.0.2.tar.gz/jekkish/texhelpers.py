import sys
from os.path import getmtime, exists, join
import re
from jinja2 import BaseLoader, TemplateNotFound


def escape_tex(value):
    """ This function allows us to redefine the jinja environment \
     to handle LaTeX environments """
    # This code, and the code that call this is courtesy of Clemens Kaposi
    # http://flask.pocoo.org/snippets/55/

    LATEX_SUBS = (
        (re.compile(r'\\'), r'\\textbackslash'),
        (re.compile(r'([{}_#%&$])'), r'\\\1'),
        (re.compile(r'~'), r'\~{}'),
        (re.compile(r'\^'), r'\^{}'),
        (re.compile(r'"'), r"''"),
        (re.compile(r'\.\.\.+'), r'\\ldots'),
    )

    newval = value
    for pattern, replacement in LATEX_SUBS:
        newval = pattern.sub(replacement, newval)
    return newval


class TeXLoader(BaseLoader):
    """ This environment loader allows us to readily customize \
    the Jinja2 BaseLoader class for our purposes """

    def __init__(self, path):
        self.path = path

    def get_source(self, environment, template):
        path = join(self.path, template)
        if not exists(path):
            raise TemplateNotFound(template)
        mtime = getmtime(path)
        with open(path) as f:
            if sys.version_info[0] < 3:
                source = f.read().decode('utf-8')  # Python 2
            else:
                source = f.read()  # Python 3
        return source, path, lambda: mtime == getmtime(path)
