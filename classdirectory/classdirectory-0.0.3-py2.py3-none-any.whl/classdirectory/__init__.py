import re
import types


class ClassDirectory(object):
    def __init__(self, module):
        if type(module) == types.ModuleType:
            self.module = module
        else:
            raise TypeError("{} is not a module.".format(module))

    def find(self, parent=object, regex=None):
        """
        Searches self.module for instances that are subclasses of the provided
        parent object.

        :param parent: The parent object.
        :type  parent: ``type``

        :param regex: Regular expression that will match object names.
        :type  regex: ``str``

        :return matched_objects: List of matching objects.
        :rtype  matched_objects: ``list``
        """
        matched_objects = []

        if regex is not None:
            regex = re.compile(regex)

        for i in dir(self.module):
            obj = getattr(self.module, i)
            filter_values = []
            filter_values.extend([isinstance(obj, type) and issubclass(obj, parent)])

            # NoneType has no attribute search
            try:
                match = regex.search(i)
            except AttributeError:
                match = True

            filter_values.append(match)

            if all(filter_values):
                matched_objects.append(obj)

        return matched_objects
