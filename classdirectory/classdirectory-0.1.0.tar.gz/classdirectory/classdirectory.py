from collections import namedtuple
import re
import types


class ClassDirectory(object):
    def __init__(self, module):
        if isinstance(module, types.ModuleType):
            self.module = module
        else:
            raise TypeError("{} is not a module.".format(module))

        self.filters = ['inheritance', 'regex']

    def find(self, parent=object, regex=None):
        """
        Searches self.module for instances that are subclasses of the provided
        parent object.

        :param parent: The parent object.
        :type  parent: ``type``

        :param regex: Regex string.
        :type  regex: ``str``

        :return matched_objects: List of matching objects.
        :rtype  matched_objects: ``list``
        """
        self.parent = parent

        self.regex = re.compile(regex)

        Suspect = namedtuple('Suspect', ['name', 'object'])
        suspects = (
            Suspect(name=i, object=getattr(self.module, i))
            for i in dir(self.module)
        )

        matched_objects = [i.object for i in self._filter(suspects)]

        return matched_objects

    def _filter(self, suspects):
        for f in self.filters:
            filter_method = getattr(self, "_{}_filter".format(f))
            suspects = filter(filter_method, suspects)
        return suspects

    def _inheritance_filter(self, s):
        return isinstance(s.object, type) and issubclass(s.object, self.parent)

    def _regex_filter(self, suspect):
        return self.regex.search(suspect.name) is not None
