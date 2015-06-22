
s = set()

print(["kabann"] + list(s))

exit()
class A(object):
    __slots__ = ["slot"]

    def hello(self):
        print "Hello"

    def slot(self):
        print "SLOT"

class B(A):
    def hello(self):
        print "B:Hello"

    def slot(self):
        print "B:Slots"

a = A()
b = B()

a.hello()
b.hello()

a.slot()
b.slot()

exit()
import humanize
import datetime



def time_ago(dt):
    """
    Return the current time ago
    """
    now = datetime.datetime.now()
    return humanize.naturaltime(now - dt)

now = datetime.datetime.now()
hrago = now - datetime.timedelta(minutes=30)

print time_ago(hrago)


exit()

import inflection

print inflection.dasherize(inflection.underscore("PawolTagiaLamizeADur"))

exit()
import os
from six.moves.urllib.parse import urlparse, urlunparse, urljoin


head = " o  "
body = "/|\ "
leg =  "/ \ "

heads = ''
bodys = ''
legs = ''

for i in range(20):
    heads += head
    bodys += body
    legs += leg

for i in range(5000):
    print heads
    print bodys
    print legs



exit()

url = "memcache://db-01.xnode.io:3306"
up = urlparse(url)
print up
print up.scheme
print up.port
print up.hostname
exit()
import inspect
import wrapt
from flask_classy import FlaskView
def inject(**kwargs):
    pass

def route(rule, **options):
    """A decorator that is used to define custom routes for methods in
    FlaskView subclasses. The format is exactly the same as Flask's
    `@app.route` decorator.
    """

    def decorator(f):
        print f.__name__
        # Put the rule cache on the method itself instead of globally
        if not hasattr(f, '_rule_cache') or f._rule_cache is None:
            f._rule_cache = {f.__name__: [(rule, options)]}
        elif not f.__name__ in f._rule_cache:
            f._rule_cache[f.__name__] = [(rule, options)]
        else:
            f._rule_cache[f.__name__].append((rule, options))

        return f

class P(FlaskView):
    @route("hello")
    def k(self):
        return "Hi"

p = P()
print p.k()

exit()

class Portfolio(object):

    @classmethod
    def extends_(cls, kls):
        if inspect.isclass(kls):
            for _name, _val in kls.__dict__.items():
                if not _name.startswith("__"):
                    setattr(cls, _name, _val)
        elif inspect.isfunction(kls):
            setattr(cls, kls.__name__, kls)
        return cls


class Q(Portfolio):
    def nice(self):
        return "NICE"

class P(Portfolio):
    def set_name(self, name):
        self.name = name

p = P()
q = Q()
#print p.__dict__


@p.extends_
def yo(self, name):
    self.set_name(name)
    print "I'm in self with %s in YO()  " % self.name

@route("hello-world")
@p.extends_
class A(object):
    phone = "123-2453-4343"
    CONST = 54

    @classmethod
    def c2(cls):
        return None

    def hello(self):
        print "This is hello"

    def index(self, name):
        self.set_name(name)
        print "I'm in self with %s " % self.name
        self.hello()

#print dir(p)
#print p.__dict__
p.hello()
p.yo("Koe")
p.index("Lola")
p.index("Nice One")

q.yo("Jones")
q.hello()
print p.phone
print p.CONST

#print f(name="Jones")
exit()


import functools

def deco(model, **kwargs):
    def wrapper(f):
        print f.__name__
        print model
        print kwargs
        return f
    return wrapper


@deco("my model", name="Jbeats")
class Global(object):
    pass


Global()
exit()




s1 = set([])
s2 = set(["B", "C", "W"])

deleted_s = s1 - s2
new_s = s2 - s1

print deleted_s
print new_s
temp3 = [x for x in s1 if x not in s2]

print temp3
exit()
from portfolio import utils

class Struct:
    def __init__(self, **entries): self.__dict__.update(entries)

a = Struct(Name="Macxis", Location="Charlotte")

print a.Name
a.Name = "Jose"
print a.Name
print a.Location

print type(a)
def test_mailer_ses():
    pass

def Mailer():
    pass


mailer = Portfolio.bind_(Mailer.init_app())()