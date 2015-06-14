import weakref

import schematec.exc
import mongoext.exc


class AbstractField(object):
    def __init__(self, descriptors):
        self.descriptors = descriptors
        self.data = weakref.WeakKeyDictionary()

    def __get__(self, instance, owner):
        return self.data.get(instance)

    def __set__(self, instance, value):
        if value is None:
            del self.data[instance]
            return

        try:
            self.data[instance] = self.descriptors(value)
        except schematec.exc.SchematecError:
            raise mongoext.exc.ValidationError(value)

    def __delete__(self, instance):
        del self.data[instance]
