#!/usr/bin/env python
"""
Command line interface to sitechantment
"""

import click
import sys
from . import SiteCheck


@click.command()
@click.option('-v', '--verbose', count=True, help="Verbosity")
@click.option('-q', '--quiet', is_flag=True, default=False)
@click.option('-d', '--dictfile', default=".aspell.en.pws")
@click.option('-l', '--lang', default="en_US")
@click.option('--update/--noupdate', default=False)
@click.argument('url')
def main(verbose, quiet, dictfile, lang, update, url):
    """Capture command line arguments and drive SiteCheck"""

    if quiet:
        verbose = -1

    sc = SiteCheck(lang=lang, verbosity=verbose, dictfile=dictfile)
    words = sc.check(url)

    if len(words) == 0:
        return 0

    if update:
        sc.update()
    print "Misspellings:"
    print "\n".join(words)
    print ""
    print "run with --update to automatically add the words to your personal"
    print "word list"

if __name__ == '__main__':
    sys.exit(main())
