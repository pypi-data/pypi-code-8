#!/usr/bin/env python

'''Filters GFF3 file annotations using metatranscriptmoic data

Usage:

    filter_gff.py <fastr> <gff> <output>

    filter_gff.py isolates clusters from a FASTR file (see below for more
detail) and then compares cluster coordinates to the annotation coordinates
of a GFF3 file. If the cluster and annotataion have sufficient overlap
(currently defined to be the annotation overlapping at least 50% of the
the cluster or the cluster encompassing the annotation, customizable
parameters will be added soon), then the annotation is written to a new
GFF3 file. In short, this script writes a new GFF3 file containing only
those annotations in a metagenome that are being expressed.
'''

__version__ = '0.0.0.3'

import argparse
from generate_fastr import *
from metameta_utilities import *
import re
import statistics
import sys

def isolate_clusters(fastr_file, log_file = None):
    '''Isolate clusters of hits from a FASTR file

    Input:

        fastr_file:
                A FASTR file.

        log_file:
                A log file to write output to. Defaults to None, which writes
                to stdout.
                
    Output:
    
        Returns the tuple (header, clusterStart, clusterEnd, localCluster)
        for each local cluster.

        header:
                The header of the FASTR entry containing the cluster

        clusterStart:
                The position of the first base in the cluster. Position
                reported with 1-index.

        clusterEnd:
                The position of the last base in the cluster. Position
                reported with 1-index.

        localCluster:
                The per base read depth data for all bases in the cluster
                given in a list. Type "metameta generate-fastr" with no
                arguments for more information on the FASTR file type.
    '''
    
    clusters = []
    localCluster = []
    for entry in entry_generator(fastr_file, 'fastr'):
        header = entry[0][1:-1]
        hitSequence = decompress_fastr(entry[1]).split('-')
        hitSequence = [int(i) for i in hitSequence]
        maxLength = len(hitSequence) - 1
        basePosition = 0
        clusterStart = 0
        clusterEnd = 0
        for base in hitSequence:
            # Start cluster
            if base != 0 and basePosition != maxLength:
                if localCluster == []:
                    clusterStart = basePosition + 1
                localCluster.append(base)
            # End of cluster if not end of entry
            elif base == 0 and localCluster != []:
                clusterEnd = basePosition
                clusterData = (header, clusterStart, clusterEnd, localCluster)
                clusters.append(clusterData)
                clusterLength = str(clusterEnd - clusterStart)
                output(clusterLength + ' base cluster isolated',\
                       args.verbosity, 2, log_file = log_file)
                localCluster = []
            # End cluster at end of entry
            elif base != 0 and basePosition == maxLength:
                if localCluster == []:
                    clusterStart = basePosition + 1
                clusterEnd = basePosition + 1
                localCluster.append(base)
                clusterData = (header, clusterStart, clusterEnd, localCluster)
                clusters.append(clusterData)
                clusterLength = str(clusterEnd - clusterStart)
                output(clusterLength + ' base cluster isolated',\
                       args.verbosity, 2, log_file = log_file)
                localCluster = []
            basePosition += 1
    return clusters

def main():
    output('Isolating clusters from ' + args.fastr[0], args.verbosity, 1,\
           log_file = args.log_file)
    rawClusters = isolate_clusters(args.fastr[0])
    output('Sorting clusters by size', args.verbosity, 1,\
           log_file = args.log_file)
    shortClusters, idealClusters, longClusters =\
                   filter_by_size(rawClusters, tuple_pos = 3,\
                                  min_length = args.min_length,\
                                  max_length = args.max_length)
    output('Reading ' + args.gff[0], args.verbosity, 1,\
           log_file = args.log_file)
    gffFile = gff_dict(args.gff[0])
    outFileHeader = ['##gff-version 3']
    outFileBody = []
    humann = {}
    output('Comparing clusters to GFF3 file annotations', args.verbosity, 1,
           log_file = args.log_file)
    for cluster in idealClusters:
        clusterHeader = cluster[0]
        clusterStart = cluster[1]
        clusterEnd = cluster[2]
        clusterDepth = cluster[3]
        for gffAnn in gffFile[clusterHeader]:
            gffSeqId = gffAnn[0]
            gffStart = int(gffAnn[3])
            gffEnd = int(gffAnn[4])
            message = 'Determining if ' + gffSeqId\
                      + ' annotates the same region as the'\
                      + ' cluster ' + clusterHeader
            output(message, args.verbosity, 2,\
                   log_file = args.log_file)
            sameGene = same_gene(clusterStart, clusterEnd, gffStart, gffEnd)
            if sameGene:
                gffHeader = '##sequence-region ' + gffSeqId + ' '\
                             + str(gffStart) + ' ' + str(gffEnd)
                outFileHeader.append(gffHeader)
                gffBody = '\t'.join(str(i) for i in gffAnn)
                outFileBody.append(gffBody)
                if args.humann_table != None:
                    try:
                        gffDbIdSegment = re.findall('inference=.+;locus_tag=',\
                                                    gffAnn[-1])[0]
                        gffDbId = re.split('=|:|;', gffDbIdSegment)[-3]
                        try:
                            assert float(gffDbId)
                        except:
                            if not gffDbId in humann:
                                humann[gffDbId] = statistics.mean(clusterDepth)
                            elif statistics.mean(clusterDepth) >\
                                 humann[gffDbId]:
                                humann[gffDbId] = statistics.mean(clusterDepth)
                    except IndexError:
                        pass
    output('Writing ' + args.output, args.verbosity, 1,\
           log_file = args.log_file)
    with open(args.output + '.gff', 'w') as out_handle:
        for header in outFileHeader:
            out_handle.write(header + '\n')
        lastLine = outFileBody[:-1]
        for body in outFileBody:
            if body == lastLine:
                out_handle.write(body)
            else:
                out_handle.write(body + '\n')
    if args.humann_table != None:
        with open(args.humann_table + '.csv', 'w') as out_handle:
            for key in humann:
                out_handle.write(key + ',' + str(humann[key]) + '\n')

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
    parser.add_argument('--humann_table',
                        default = None,
                        help = 'output file for humann csv')
    parser.add_argument('--min_length',
                        type = int,
                        default = 100,
                        help = 'Minimum length cluster to keep')
    parser.add_argument('--max_length',
                        type = int,
                        default = None,
                        help = 'Maximum length cluster to keep')
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
        output(args.gff[0] + ' successfully filtered', args.verbosity, 1,
               log_file = args.log_file)
    output('Exiting filter_gff.py', args.verbosity, 1,\
           log_file = args.log_file)

    sys.exit(0)
