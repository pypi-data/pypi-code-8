#/usr/env python

class A(object):
    def upper(self):
        return "A"

class B(object):
    def upper(self):
        return "B"

class EFPContainer(object):
    def __init__(self, *args):
        r = []
        for i in args:
            if type(i) is list:
                r += i
            else:
                r += [i]
        self.efps = r

    def __getattr__(self, name):
        def wrapper(*args, **kargs):
            return EFPContainer([getattr(i,name)(*args,**kargs) for i in self.efps])
        return wrapper

    def EPFs(self):
        return self.efps

print Container([A(), A(), A()],
                [B(), B(), B()],["hello", "bye"], "hello").upper().unpack()
