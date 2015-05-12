from os import path
from sys import modules


def group(obj):
    group = obj.__class__.__name__
    if group == "function":
        filename = modules[obj.__module__].__file__
        group = path.splitext(path.basename(filename))[0]
    return group


class Foo(object):
    def foo(self):
        print "from inside I am {}".format(self.__class__.__name__)


def bar():
    pass


f = Foo()
f.foo()  # prints Foo
print "f.foo's name is {}".format(f.foo.__name__)  # prints foo
print "f.foo's group is {}".format(group(f.foo))  # prints instancemethod

bar()
print "bar's name is {}".format(bar.__name__)
print "bar's group is {}".format(group(bar))
