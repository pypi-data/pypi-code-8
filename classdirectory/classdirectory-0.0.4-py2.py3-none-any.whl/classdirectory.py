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

        :param regex: Compiled regex object that will match object names.
        :type  regex: compiled regex object

        :return matched_objects: List of matching objects.
        :rtype  matched_objects: ``list``
        """
        matched_objects = []

        for i in dir(self.module):
            obj = getattr(self.module, i)
            filter_values = []
            filter_values.extend([isinstance(obj, type) and issubclass(obj, parent)])

            if regex:
                match = regex.search(i)
                filter_values.append(match)

            if all(filter_values):
                matched_objects.append(obj)

        return matched_objects
