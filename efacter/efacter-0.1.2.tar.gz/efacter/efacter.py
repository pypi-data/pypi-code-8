#!/usr/bin/env python

from Facter import Facter
import json, sys
from optparse import OptionParser
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter
from pygments.styles import native

def getOptions ():
    usage = "usage: %prog [options] <fact.element1.element2> [anotherFact.element1] [andAnother] ... "
    optionparser = OptionParser(usage=usage)
    optionparser.add_option("-j", "--json", dest="jsonOutput", default=False, action="store_true",
            help="Output JSON")
    optionparser.add_option("-o", "--json-one-string", dest="oneString", default=4, action="store_const", const=None,
            help="Output JSON as one string (without indent)")
    optionparser.add_option("-d", "--delimiter", dest="delimiter", default='.', action="store", metavar="DELIMITER",
            help="Delimiter for elements (default is '.'))")
    optionparser.add_option("-n", "--no-colour", dest="noColour", default=False, action="store_true",
            help="Disable colours in the output")
    (options, args) = optionparser.parse_args()
    if len(args) < 1:
        optionparser.error("You need to provide at least one argument")
    return options, args


def getData (args, options):
    # Get Data and prepare JsonDump
    facter = Facter(args)
    facter.separator = options.delimiter
    return facter.pieces()


def makeJson (j, indent, noColour):
        j = json.dumps(j, indent=indent)
        if not noColour: j = highlight(j, JsonLexer(), TerminalFormatter()).rstrip('\n')
        return j

def main():
    (options, args) = getOptions()
    chunks = getData(args, options)
    if options.jsonOutput:
        print makeJson(chunks, options.oneString, options.noColour)
    else:
        if options.noColour:
            headerStyle = resetStyle = ''
        else:
            headerStyle = '\033[1m\033[92m'
            resetStyle = '\033[0m'
        for piece in args:
            print "%s: %s" % (headerStyle + piece + resetStyle, makeJson(chunks[piece], options.oneString, options.noColour))

if __name__ == "__main__":
    sys.exit(main())
