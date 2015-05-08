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

__version__ = '0.0.0.2'

from metameta_utilities import *
import re

def gff_dict(gff_file):
    '''Reads a GFF file of important information for annotation purposes

    Input:

        gff_file:
                The GFF3 file to be read.

    Output:

            A dictionary where each key is a contig header. Each value is a
            list of all the annotations for that contig. Each item in the list
            is a tuple containing the gene name, the start of the gene, and
            the end of the gene.
    '''
    
    annotations = {}
    for entry in entry_generator(gff_file, 'gff3'):
        start = int(entry[3]) - 1
        end = int(entry[4]) - 1
        geneLocation = entry[-1][:-1]
        header = entry[0]
        gene = re.split('(product=)|(rpt_family=)', geneLocation)[-1]
        annotation = (gene, start, end)
        if header in annotations:
            annotations[header].append(annotation)
        else:
            annotations[header] = [annotation]
    return annotations

def same_gene(clusterStart, clusterEnd, gffStart, gffEnd):
    '''Determines if a cluster and annotation on a contig cover the same gene

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
    # GFF overlaps clusters by at least 50%
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
    '''Generator for a stats file (or any tab-delimted file)

    Input:

        stats_file:
                The stats file to be read.

    Output:

            A tab-delimited list of each line of the stats file.
    '''
    
    with open(stats_file, 'rU') as in_handle:
        for line in in_handle:
            sepLine = line[:-1].split('\t')
            yield sepLine

def main(stats_file, gff_file):
    output('Generating dicitonary from ' + gff_file, args.verbosity, 1,\
           log_file = args.log_file)
    annotations = gff_dict(gff_file)
    fileName = stats_file.replace('.txt', '.ann')
    with open(fileName, 'w') as out_handle:
        for line in read_stats(stats_file):
            if line[0] == 'Header':
                firstLine = ''
                for item in line:
                    firstLine = firstLine + item + '\t'
                firstLine = firstLine + 'GFF Start\tGFF End\tGene\n'
                out_handle.write(firstLine)
            else:
                geneAnnotation = ''
                annHeader = line[0]
                if annHeader in annotations:
                    for gffData in annotations[annHeader]:
                        gffStart = gffData[1]
                        gffEnd = gffData[2]
                        clusterStart = int(line[1])
                        clusterEnd = int(line[2])
                        message = 'Determining if ' + gffData[0] +\
                                  ' annotates the same region as the'\
                                  + ' cluster ' + annHeader
                        output(message, args.verbosity, 2,\
                               log_file = args.log_file)
                        sameGene = same_gene(clusterStart, clusterEnd,\
                                             gffStart, gffEnd)
                        if sameGene:
                            message = 'Appending gene annotation to'\
                                      + ' cluster'
                            output(message ,args.verbosity, 2,\
                                   log_file = args.log_file)
                            geneAnnotation = str(gffStart) + '\t' + \
                                             str(gffEnd) + '\t' + gffData[0]
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
            output('Verifying ' + args.gff[0], args.verbosity, 1,\
                   log_file = args.log_file)
            verify_file(args.gff[0])
        main(args.stats, args.gff[0])
    output('Exiting annotate_clusters.py', args.verbosity, 1,\
           log_file = args.log_file)

    sys.exit(0)
