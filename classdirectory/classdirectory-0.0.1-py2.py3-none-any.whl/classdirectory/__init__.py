class ClassDirectory(object):
    def __init__(self, module):
        self.module = module

    def find(self, parent=object):
        """
        Searches self.module for instances that are subclasses of the provided
        parent object.

        :param parent: The parent object.
        :type  parent: ``type``

        :return matched_objects: List of matching objects.
        :rtype  matched_objects: ``list``
        """
        matched_objects = []
        for i in dir(self.module):
            obj = getattr(self.module, i)
            if isinstance(obj, type) and issubclass(obj, parent):
                matched_objects.append(obj)

        return matched_objects
