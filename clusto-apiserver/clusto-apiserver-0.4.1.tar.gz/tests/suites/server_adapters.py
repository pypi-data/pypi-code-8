#!/usr/bin/env python
#
# -*- mode:python; sh-basic-offset:4; indent-tabs-mode:nil; coding:utf-8 -*-
# vim:set tabstop=4 softtabstop=4 expandtab shiftwidth=4 fileencoding=utf-8:
#

import bottle
import port_for
import sys
import unittest
import util


# Select a random port to spin up this testing server
SERVER_ADAPTERS = (
    ('wsgiref', bottle.WSGIRefServer,),
    ('paste', bottle.PasteServer,),
    ('gunicorn', bottle.GunicornServer,),
    ('cherrypy', bottle.CherryPyServer,),
    ('flup', bottle.FlupFCGIServer,),
)


# class ServerAdapter200(unittest.TestCase):
#
#    def __init__(self, functionname, function):
#        f = functools.partial(function)
#        f.__doc__ = 'At least one ShellDoc example for %s.%s' % (function.__module__, functionname,)
#        methodname = 'test_adapter_%s_%s' % (
#            function.__module__.replace('.', '_'),
#            functionname.replace('.', '_'),
#        )
#        self.__setattr__(methodname, f)
#        unittest.TestCase.__init__(self, methodname)
#
#    def shelldoc(self, function):
#        "ShellDoc completeness partial check"
#        # we don't care about strings here, just that there is at least 1 example
#        finder = doctest.DocTestFinder(
#            parser=shelldoctest.ShellDocTestParser(),
#            exclude_empty=False,
#        )
#        shelldocs = finder.find(function)
#        for sd in shelldocs:
#            self.assertGreater(
#                len(sd.examples), 0,
#                msg='All public functions must have at least 1 shell example'
#            )


def test_cases():
    adapter_testsuite = unittest.TestSuite()

    for s, o in SERVER_ADAPTERS:
        port = port_for.select_random()
        obj = o()
        print obj
        obj.run(util.QuietHandler)
        print obj
        obj.shutdown()
        # THREADS[s][0].start()
        # count = 0
        # while not util.ping(port) and count < 50:
        #    count += 1

    return adapter_testsuite


def main():
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_cases())
    return (len(result.errors) + len(result.failures)) > 0


if __name__ == '__main__':
    sys.exit(main())
