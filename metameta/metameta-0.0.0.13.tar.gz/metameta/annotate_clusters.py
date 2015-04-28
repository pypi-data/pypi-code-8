#!/usr/bin/env python

'''annotate clusters in a stats.txt file

Usage:

    annotate_clusters.py [--log_file] [--verbose] [--version] [--verify]
                         <stats> <gff>

    annotate_clusters.py adds three columns to a stats file with data from
a GFF file. Clusters and GFF annotations are compared to see if they
overlap. If there is sufficient overlap, then the GFF annotation start, GFF
annotation end, and GFF annotation are added to the stats file.

This tool is specifically designed to extract gene and/or family names from
the GFF3 files produced by PROKKA.

The new file is titled <fastr>.stats.ann and has the following tab-delimited
columns:

Header
Cluster Start
Cluster End
Average Read Depth
GFF Start
GFF End
Gene
'''

__version__ = '0.0.0.1'

from metameta_utilities import *
import re

def same_gene(clusterStart, clusterEnd, gffStart, gffEnd):
    '''determines if a cluster and annotation on a contig cover the same gene

    Input:

        clusterStart:
                The start of the cluster.

        clusterEnd:
                The end of the cluster.

        gffStart:
                The start of the GFF annotation.

        gffEnd:
                The end of the GFF annotation.

    Output:

            Boolean: True or False
    '''
    
    sameGene = False
    # Cluster encompasses GFF
    if clusterStart <= gffStart and clusterEnd >= gffEnd:
        sameGene = True
    # GFF encompasses Cluster
    elif clusterStart >= gffStart and clusterEnd <= gffEnd:
        sameGene = True
    else:
        overlap = 0
        if clusterEnd > gffEnd and clusterStart > gffStart:
            overlap = gffEnd - clusterStart
        elif gffEnd > clusterEnd and gffStart > clusterStart:
            overlap = clusterEnd - gffStart
        overlapRatio = float(overlap)/float(clusterEnd - clusterStart)
        if overlapRatio >= 0.5:
            sameGene = True
    return sameGene

def read_stats(stats_file):
    '''generator for a stats file

    Input:

        stats_file:
                The stats file to be read

    Output:

            A tab-delimited list of each line of the stats file
    '''
    
    with open(stats_file, 'rU') as in_handle:
        for line in in_handle:
            sepLine = line[:-1].split('\t')
            yield sepLine

def main(stats_file, gff_file):
    annotations = {}
    for entry in entry_generator(gff_file, 'gff3'):
        header = entry[0]
        start = int(entry[3]) - 1
        end = int(entry[4]) - 1
        geneLocation = entry[-1][:-1]
        gene = re.split('(product=)|(rpt_family=)', geneLocation)[-1]
        annotations[header] = (gene, start, end)
    with open(stats_file.replace('.txt', '.ann'), 'w') as out_handle:
        for line in read_stats(stats_file):
            if line[0] == 'Header':
                firstLine = ''
                for item in line:
                    firstLine = firstLine + item + '\t'
                firstLine = firstLine + 'GFF Start\tGFF End\tGene\n'
                out_handle.write(firstLine)
            else:
                geneAnnotation = '\t\t'
                if line[0] in annotations:
                    gffData = annotations[line[0]]
                    gffStart = gffData[1]
                    gffEnd = gffData[2]
                    clusterStart = int(line[1])
                    clusterEnd = int(line[2])
                    sameGene = same_gene(clusterStart, clusterEnd,\
                                         gffStart, gffEnd)
                    if sameGene:
                        geneAnnotation = str(gffStart)\
                                         + '\t' + str(gffEnd) + '\t' +\
                                         gffData[0]
                toWrite = ''
                for item in line:
                    toWrite = toWrite + item + '\t'
                toWrite = toWrite + geneAnnotation + '\n'
                out_handle.write(toWrite)
                            
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = __doc__,
                                        formatter_class = argparse.\
                                        RawDescriptionHelpFormatter)
    parser.add_argument('stats',
                        default = None,
                        nargs = '?',
                        help = 'the stats file from filter_fastr')
    parser.add_argument('gff',
                        type = file_type,
                        default = None,
                        nargs = '?',
                        help = 'GFF3 file with annotations')
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
    elif args.stats == None and args.gff == None:
        print(__doc__)
    elif args.stats == None or args.gff == None:
        message = 'Need to specify a stats file and a GFF3 file.'
        output(message, args.verbosity, 0, fatal = True)
    else:
        if args.verify:
            verify_file(args.gff[0])
        main(args.stats, args.gff[0])

    sys.exit(0)
