#!/usr/bin/env python3
"""
Usage: offyt [-v] PLAYLIST [OUTPUTDIR]
"""

import docopt
import errno
import filelock
import os
import re
import sys
import youtube_dl

arguments = docopt.docopt(__doc__, version='offyt 0.1.3')

outputdir = arguments['OUTPUTDIR'] or "./"
playlist = arguments['PLAYLIST']

ydl_opts = {
    'nocheckcertificate': True,
    'outtmpl': os.path.join(outputdir, "%(uploader_id)s/%(title)s-[%(id)s].%(ext)s"),
    'quiet': not arguments['-v'],
    'restrictfilenames': True,
}

rx_id = re.compile(r'\[(.*?)\]\..{3,4}$')

lock = filelock.FileLock(os.path.join(outputdir, ".lock"))
try:
    lock.acquire(timeout=1)
except filelock.Timeout:
    if arguments['-v']:
        print('already running')
    sys.exit(0)
else:
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:

        ydl.download([playlist])

        info = ydl.extract_info(playlist, download=False)
        ids = set([e['id'] for e in info['entries']])

        for root, dirs, files in os.walk(outputdir):
            for name in files:
                match = rx_id.search(name)
                if match and match.group(1) not in ids:
                    os.unlink(os.path.join(root, name))

        for root, dirs, files in os.walk(outputdir):
            for dirname in dirs:
                try:
                    os.rmdir(os.path.join(root, dirname))
                except OSError as ex:
                    if ex.errno != errno.ENOTEMPTY:
                        raise
finally:
    lock.release()
