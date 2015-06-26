# -*- coding: utf-8 -*-
'''
© 2012-2013 eBay Software Foundation
Authored by: Tim Keefer
Licensed under CDDL 1.0
'''

import os
import sys
import gevent

from optparse import OptionParser

sys.path.insert(0, '%s/../' % os.path.dirname(__file__))

from common import dump
from ebaysdk.finding import Connection as finding
from ebaysdk.http import Connection as html
from ebaysdk.parallel import Parallel
from ebaysdk.exception import ConnectionError

def init_options():
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)

    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug", default=False,
                      help="Enabled debugging [default: %default]")
    parser.add_option("-y", "--yaml",
                      dest="yaml", default='ebay.yaml',
                      help="Specifies the name of the YAML defaults file. [default: %default]")
    parser.add_option("-a", "--appid",
                      dest="appid", default=None,
                      help="Specifies the eBay application id to use.")

    (opts, args) = parser.parse_args()
    return opts, args


def run(opts):

    try:
        p = Parallel()
        apis = []

        api1 = finding(debug=opts.debug, appid=opts.appid, config_file=opts.yaml)
        api2 = finding(debug=opts.debug, appid=opts.appid, config_file=opts.yaml)
        api3 = finding(debug=opts.debug, appid=opts.appid, config_file=opts.yaml)
        api4 = finding(debug=opts.debug, appid=opts.appid, config_file=opts.yaml)

        r1 = api1.execute('findItemsAdvanced', {'keywords': 'python'})
        r2 = api2.execute('findItemsAdvanced', {'keywords': 'perl'})
        r3 = api3.execute('findItemsAdvanced', {'keywords': 'java'})
        r4 = api4.execute('findItemsAdvanced', {'keywords': 'ruby'})
        
        print len(r1.dict())
        print len(r2.dict())
        print len(r3.dict())
        print len(r4.dict())


        ##if p.error():
        #    print(p.error())

        #for api in apis:
        #    dump(api)

    except ConnectionError as e:
        print(e)
        print(e.response.dict())

if __name__ == "__main__":
    (opts, args) = init_options()
    run(opts)
