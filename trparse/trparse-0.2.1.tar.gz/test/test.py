import glob

import trparse

test_files = glob.glob('*.txt')

for test_file in test_files:
    with open(test_file) as f:
        result = trparse.load(f)
        print "FILE %s" % test_file
        print result
