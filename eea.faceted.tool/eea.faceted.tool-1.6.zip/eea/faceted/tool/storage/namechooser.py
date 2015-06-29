import re
from zope.interface import implements

from zope.app.container.interfaces import INameChooser
from zope.app.container.contained import NameChooser

ATTEMPTS = 10000

class PortalTypeNameChooser(NameChooser):
    """A name chooser for portal types.
    """

    implements(INameChooser)

    def __init__(self, context):
        self.context = context

    def checkName(self, name, object):
        return True

    def chooseName(self, name, object):
        container = self.context
        name = name or getattr(object, 'title', '')
        safe = re.compile(r'[^_A-Za-z0-9\.\-\s]')
        name = safe.sub('', name)
        name = name or object.__class__.__name__
        name = name.strip()

        i = 0
        new_name = name
        while new_name in container.objectIds() and i <= ATTEMPTS:
            i += 1
            new_name = "%s-%d" % (name, i)

        self.checkName(new_name, object)
        return new_name.encode('utf-8')
