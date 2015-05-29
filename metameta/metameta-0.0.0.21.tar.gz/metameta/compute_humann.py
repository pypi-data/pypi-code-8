#!/usr/bin/env python

'''Finds abundance of genes for metagenome on metagenome

Usage:

    compute_humann [--log_file] [--verbose] [--version] [--verify] <fastr>
                   <gff> <output>
'''

import argparse
from generate_fastr import *
from metameta_utilities import *
import re
import statistics
import sys

def main():
    output('Reading ' + args.gff[0], args.verbosity, 1,\
           log_file = args.log_file)
    gffFile = gff_dict(args.gff[0])
    with open(args.output + '.csv', 'w') as out_handle:
        for entry in entry_generator(args.fastr[0], 'fastr'):
            header = entry[0].lstrip('+').rstrip('\n')
            if header in gffFile:
                for ann in gffFile[header]:
                    gffStart = int(ann[3]) - 1
                    gffEnd = int(ann[4]) - 1
                    depthData = decompress_fastr(entry[1]).split('-')
                    depthData = [int(i) for i in depthData[gffStart:gffEnd]]
                    if len(depthData) > 0:
                        average = statistics.mean(depthData)
                        try:
                            gffDbIdSegment = re.findall('inference=.+;locus_tag=',\
                                                        ann[-1])[0]
                            gffDbId = re.split('=|:|;', gffDbIdSegment)[-3]
                            try:
                                assert float(gffDbId)
                            except:
                                out_handle.write(gffDbId + ',' + str(average) + '\n')
                        except IndexError:
                            pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = __doc__,
                                        formatter_class = argparse.\
                                        RawDescriptionHelpFormatter)
    parser.add_argument('fastr',
                        type = file_type,
                        default = None,
                        nargs = '?',
                        help = 'FASTR file containing read depth data'\
                        + ' for a metatranscriptome mapped onto a metagenome')
    parser.add_argument('gff',
                        type = file_type,
                        default = None,
                        nargs = '?',
                        help = 'GFF3 file with annotations for the same'\
                        + ' metagenome as the FASTR file')
    parser.add_argument('output',
                        default = None,
                        nargs = '?',
                        help = 'name of GFF3 file to write')
    parser.add_argument('-l', '--log_file',
                        default = None,
                        help = 'log file to print all messages to')
    parser.add_argument('-v', '--verbosity',
                        action = 'count',
                        default = 0,
                        help = 'increase output verbosity')
    parser.add_argument('--verify',
                        action = 'store_true',
                        help = 'verify input files before use')
    parser.add_argument('--version',
                        action = 'store_true',
                        help = 'prints tool version and exits')
    args = parser.parse_args()

    if args.version:
        print(__version__)
    elif args.fastr == None:
        print(__doc__)
    elif args.gff == None:
        message = 'Must specify a FASTR, GFF3, and output file'
        output(message, args.verbosity, 0,\
               log_file = args.log_file)
    else:
        if args.verify:
            output('Verifying ' + args.fastr[0], args.verbosity, 1,\
                   log_file = args.log_file)
            verify_file(args.fastr[0], log_file = args.log_file)
            output(args.fastr[0] + ' is a valid', args.verbosity, 1,\
                   log_file = args.log_file)
            output('Verifying ' + args.gff[0], args.verbosity, 1,\
                   log_file = args.log_file)
            verify_file(args.gff[0], log_file = args.log_file)
            output(args.gff[0] + ' is a valid', args.verbosity, 1,\
                   log_file = args.log_file)
        main()

    sys.exit(0)

