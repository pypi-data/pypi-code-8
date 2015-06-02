#!/usr/bin/env python
# Parse hints from SDL_hints.h (passed in stdin) writing
# python-compatible version to stdout.

import sys
import re

hint = re.compile('#define.*(SDL_HINT\w+).*("\w+")')
for line in sys.stdin:
    match = hint.match(line)
    if match:
        sys.stdout.write("%s = %s\n" % (match.group(1), match.group(2)))
