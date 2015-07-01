#!/usr/bin/env python
import sys

if sys.argv[1:] == ['--disable-pip-version-check', 'freeze']:
    sys.stdout.write('''\
    picky==0.0.dev0
    testfixtures==4.1.2
    ''')
    sys.exit(0)
elif sys.argv[1:] == ['--disable-pip-version-check', '--version']:
    sys.stdout.write('''\
    pip fake from /some/path
    ''')
    sys.exit(0)
else:
    raise TypeError(repr(sys.argv))

