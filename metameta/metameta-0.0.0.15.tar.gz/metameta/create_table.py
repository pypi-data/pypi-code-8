#!/usr/bin/env python

'''create a table metatranscriptomic coverage by sample

Usage:

    annotate_clusters.py [--log_file] [--verbose] [--version] [--verify]
                         <table> <gff> <[ann]>

    Reads a GFF file and multiple annotation files from annotate_clusters.py
to compile a tab-delimited table where each row is a different annotation
and each column is a different annotation file. This requires that each
annotation file used the same GFF file for it's annotations. Each cell
contains the average metatranscriptomic coverage of a given gene in a
given metatranscriptome.
'''

__version__ = '0.0.0.1'

from annotate_clusters import *
from metameta_utilities import *
import sys

def main(stats_files, gff_file, table_file):
    annotations = gff_dict(gff_file)
    headers = []
    genes = {}
    # "Flatten" annotations for faster identification of unique annotations
    output('Building annotation dictionary', args.verbosity, 1,\
           log_file = args.log_file)
    for key in annotations:
        for orf in annotations[key]:
            newKey = [key]
            for part in orf:
                newKey.append(part)
            newKey = tuple(newKey)
            genes[newKey] = [0 for file in stats_files]
    location = 0
    for file in stats_files:
        output('Analyzing ' + file, args.verbosity, 1,\
               log_file = args.log_file)
        headers.append(file.split('.')[0].split('/')[-1])
        # lastKey used to identify multiple clusters within a single annotation
        lastKey = ('', '', '', '')
        repeatDepths = []
        repeatLengths = []
        statsFile = read_stats(file)
        # Skip the headers line
        next(statsFile)
        for line in statsFile:
            # Prevent crashing if there is no annotation for a cluster
            try:
                ann = (line[0], line[6], int(line[4]), int(line[5]))
            except ValueError:
                ann = (line[0], line[6], line[4], line[5])
            # Identify repeats within an annotation
            if lastKey[1] != '' and ann == lastKey:
                lengthAnn = ann[3] - ann[2]
                repeatLengths.append(lengthAnn)
                repeatDepths.append(float(line[3]))
            # When repeat terminates, calculate average and store data
            elif lastKey[1] != '' and ann != lastKey:
                weightedAverages = []
                totalLength = sum(repeatLengths)
                for average, length in zip(repeatDepths, repeatLengths):
                    weightedAverage = float(average)*float(length)/totalLength
                    weightedAverages.append(weightedAverage)
                modifiedAverage = sum(weightedAverages)
                genes[lastKey][location] = modifiedAverage
                repeatDepths = []
                repeatLengths = []
            lastKey = ann
        # Ensures that last cluster in data is stored if it has an annotation
        if lastKey[1] != '':
            weightedAverages = []
            totalLength = sum(repeatLengths)
            for average, length in zip(repeatDepths, repeatLengths):
                weightedAverage = float(average)*float(length)/totalLength
                weightedAverages.append(weightedAverage)
            modifiedAverage = sum(weightedAverages)
            genes[lastKey][location] = modifiedAverage
        location += 1
    output('Writing table to ' + table_file, args.verbosity, 1,\
           log_file = args.log_file)
    with open(table_file, 'w') as out_handle:
        theHeaders = ''
        for i in headers:
            theHeaders = theHeaders + '\t' + i
        out_handle.write(theHeaders + '\n')
        for key in genes:
            theLine = tuple(key)[1]
            for depth in genes[key]:
                theLine = theLine + '\t' + str(depth)
            out_handle.write(theLine + '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = __doc__,
                                        formatter_class = argparse.\
                                        RawDescriptionHelpFormatter)
    parser.add_argument('table',
                        default = None,
                        nargs = '?',
                        help = 'the output file')
    parser.add_argument('gff',
                        type = file_type,
                        default = None,
                        nargs = '?',
                        help = 'GFF3 file with annotations')
    parser.add_argument('ann',
                        default = None,
                        nargs = '*',
                        help = 'annotation file from annotate_clusters.py')
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
    elif args.ann == None and args.gff == None:
        print(__doc__)
    elif args.ann == None or args.gff == None or args.table == None:
        message = 'Need to specify one or more stats file, a GFF3 file, and an output file.'
        output(message, args.verbosity, 0, fatal = True)
    else:
        if args.verify:
            output('Verifying ' + args.gff[0], args.verbosity, 1,\
                   log_file = args.log_file)
            verify_file(args.gff[0])
        main(args.ann, args.gff[0], args.table)
    output('Exiting create_table.py', args.verbosity, 1,\
           log_file = args.log_file)

    sys.exit(0)
