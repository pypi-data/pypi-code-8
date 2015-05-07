#!/usr/bin/env python

'''Filters FASTR data and reports statistics

Usage:

    filter_fastr.py [--log_file] [--verbose] [--version] [--verify]
                    [--min_length] [--max_length] <fastr>

    filter_fastr.py reads a fastr file, isolates clusters, and seperates
clusters by size: clusters below a certain length, clusters above a 
certain length, and all clusters in-between the specified lengths.
Each respective category is written as:

    <fastr>.short.fastr
    <fastr>.long.fastr
    <fastr>.ideal.fastr

Additionally, statistical information on each category is written in:

    <fastr>.short.stats.txt
    <fastr>.long.stats.txt
    <fastr>.ideal.stats.txt

    A cluster is defined as all consecutive bases containing non-zero read
depth data flanked by bases containing read depths of zero or the end of
the entry. Two examples follow:

        200x0-3x10-4x11-7x18-50x15

The above entry has a single cluster consisting of the read depth data:
    3x10-4x11-7x18-50x15
This is one cluster because it is flanked by bases of read depth zero
on one end and the end of the entry on the other.

        150x0-10x3-20x6-250x7-8-9-10x0-50x1-20x2-30x3-12x7-80x0

The above entry has two clusters:
    10x3-20x6-250x7-8-9
    50x1-20x2-30x3-12x7
Both clusters are flanked by bases of read depth zero. Thus this
function reports two reads with the same heading since they are from
the same FASTR heading.

Each row in the stats file is a row with four following tab-delimited columns:

Header
Cluster Start
Cluster End
Average Read Depth
'''

__version__ = '0.0.0.3'

import argparse
from generate_fastr import compress_fastr, decompress_fastr, write_fastr
from metameta_utilities import *

def filter_by_size(unfiltered_list, tuple_pos = None, min_length = None,\
                   max_length = None):
    '''Filters a list of lists, or tuples, by size

    Input:

        unfiltered_list:
                A list of lists or tuples to be filtered by size.

        tuplePos:
                If unfiltered_list is a list of tuples, this argument
                specifies which item of the tuple contains the list
                to sort by length. Default is None.

        min_length:
                The minimum length a list must be to pass filtering.
                Default is None.

        max_length:
                The maximum length a list must be to pass filtering.
                Default is None.

    Output:

        Returns the tuple (shortLists, idealLists, longLists)

        shortLists:
                A list of the lists or tuples with length less than min_length.

        idealLists:
                A list of lists or tuples with length greater than or equal to
                min_length and less than or equal to max_length.

        longLists:
                A list of the lists or tuples with length greater than
                max_length.        
    '''
    
    shortLists = []
    idealLists = []
    longLists = []
    listsToFilter = []
    if tuple_pos != None:
        for subTuple in unfiltered_list:
            listsToFilter.append(subTuple[tuple_pos])
    else:
        for subList in unfiltered_list:
            listsToFilter.append(subList)
    position = 0
    for subList in listsToFilter:
        subLength = len(subList)
        if min_length != None and subLength < min_length:
            message = str(subList) + ' in '+ str(unfiltered_list) + \
                      ' is less than the minimum length'\
                      + str(min_length)
            output(message, args.verbosity, 2, log_file = args.log_file)
            shortLists.append(unfiltered_list[position])
        elif max_length != None and subLength > max_length:
            message = str(subList) + ' in '+ str(unfiltered_list) + \
                      ' is greater than the maximum length'\
                      + str(max_length)
            output(message, args.verbosity, 2, log_file = args.log_file)
            longLists.append(unfiltered_list[position])
        else:
            message = str(subList) + ' in '+ str(unfiltered_list) + \
                      ' is within the length parameters: '\
                      + 'minimum length = ' + str(min_length) + \
                      ' and maximum length = ' + str(max_length)
            output(message, args.verbosity, 2, log_file = args.log_file)
            idealLists.append(unfiltered_list[position])
        position += 1
    return (shortLists, idealLists, longLists)

def get_averages(in_list, tuple_pos = None):
    '''Gets the averages of a list of lists

    Input:

        in_list:
                A list of lists or tuples to get the averages of.

        tuplePos:
                If in_list is a list of tuples, this argument specifies
                which position of the tuple contains the list to be averaged.

    Output:

        Returns a list of floats containg the averages of each list in in_list.
        If in_list is a list of tuples, then a list of tuples is returned
        with the original list in the tuple replaced by the float average value.
    '''
    
    averagesList = []
    listsToAverage = []
    if tuple_pos != None:
        for subTuple in in_list:
            listsToAverage.append(subTuple[tuple_pos])
    else:
        for subList in in_list:
            listsToAverage.append(subList)
    position = 0
    for subList in listsToAverage:
        temporaryData = []
        average = float(sum(subList))/float(len(subList))
        # Reconstruct original tuple with list average replacing the list
        if tuple_pos != None:
            count = 0
            for item in in_list[position]:
                if count != tuple_pos:
                    temporaryData.append(item)
                else:
                    temporaryData.append(average)
                count += 1
            temporyData = tuple(temporaryData)
        else:
            temporaryData = average
        averagesList.append(temporaryData)
        position += 1
    return averagesList

def isolate_clusters(fastr_file):
    '''Isolate clusters of hits from a FASTR file

    Input:

        fastr_file: A FASTR file

    Output:
    
        Returns the tuple (header, clusterStart, clusterEnd, localCluster)
        for each local cluster.

        header:
                The header of the FASTR entry containing the cluster

        clusterStart:
                The position of the first base in the cluster. Position
                reported with 0-index.

        clusterEnd:
                The position of the last base in the cluster. Position
                reported with 0-index.

        localCluster:
                The per base read depth data for all bases in the cluster
                given in the FASTR format (non-compressed). Type
                "metameta generate-fastr" with no arguments for more
                information on the FASTR file type.
    '''
    
    clusters = []
    localCluster = []
    for entry in entry_generator(fastr_file, 'fastr'):
        header = entry[0][1:-1]
        hitSequence = decompress_fastr(entry[1]).split('-')
        maxLength = len(hitSequence) - 1
        basePosition = 0
        clusterStart = 0
        clusterEnd = 0
        for base in hitSequence:
            # Start cluster
            if base != 0 and basePosition != maxLength:
                if localCluster == []:
                    clusterStart = basePosition
                localCluster.append(base)
            # End of cluster if not end of entry
            elif base == 0 and localCluster != []:
                clusterEnd = basePosition - 1
                clusterData = (header, clusterStart, clusterEnd, localCluster)
                clusters.append(clusterData)
                clusterLength = str(len(clusterEnd - clusterStart))
                output(clusterLength + ' base cluster isolated', args.verbosity, 2,\
                       log_file = args.log_file)
                localCluster = []
            # End cluster at end of entry
            elif base != 0 and basePosition == maxLength:
                if localCluster == []:
                    clusterStart = basePosition
                clusterEnd = basePosition
                localCluster.append(base)
                clusterData = (header, clusterStart, clusterEnd, localCluster)
                clusters.append(clusterData)
                clusterLength = str(len(clusterEnd - clusterStart))
                output(clusterLength + ' base cluster isolated', args.verbosity, 2,\
                       log_file = args.log_file)
                localCluster = []
            basePosition += 1
    return clusters

def main(in_file, min_length = None, max_length = None):
    output('Isolating Clusters', args.verbosity, 1, log_file = args.log_file)
    rawClusters = isolate_clusters(in_file)
    output('Sorting clusters by size', args.verbosity, 1, log_file = args.log_file)
    shortClusters, idealClusters, longClusters =\
                   filter_by_size(rawClusters, tuplePos = 3,\
                                  min_length = min_length,\
                                  max_length = max_length)
    categories = ((shortClusters, 'short'), (idealClusters, 'ideal'),\
                  (longClusters, 'long'))
    for category in categories:
        headers = []
        readDepthSequences = []
        for cluster in category[0]:
            headers.append(cluster[0])
            read_depth_sequences.append(cluster[3])
        file_name = in_file.replace('fastr', category[1] + '.fastr')
        location = 0
        for depthSequence in readDepthSequences:
            depthSequence = compress_fastr(depthSequence)
            readDepthSequence[location] = depthSequence
            location += 1
        output('Writing ' + file_name, args.verbosity, 1, log_file = args.log_file)
        write_fastr(headers, readDepthSequences, file_name)
        clusterDepthAverages = get_averages(category[0], tuplePos = 3)
        out_file = file_name.replace('fastr', 'stats.txt')
        output('Writing ' + out_file, args.verbosity, 1, log_file = args.log_file)
        with open(out_file, 'w') as out_handle:
            headerRow = 'Header\tCluster Start\tCluster End\t'\
                        + 'Average Read Depth'
            out_handle.write(headerRow + '\n')
            for item in clusterDepthAverages:
                line = ''
                for i in item:
                    line = line + str(i) + '\t'
                line = line[:-1]
                out_handle.write(line + '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = __doc__,
                                        formatter_class = argparse.\
                                        RawDescriptionHelpFormatter)
    parser.add_argument('fastr',
                        type = file_type,
                        default = None,
                        nargs = '?',
                        help = 'FASTR file to be filtered')
    parser.add_argument('--min_length',
                        type = int,
                        default = 76,
                        help = 'Minimum number of consecutive hits to keep')
    parser.add_argument('--max_length',
                        type = int,
                        default = None,
                        help = 'Maximum number of consecutive hits to keep')
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
    else:
        if args.verify:
            output('Verifying ' + args.fastr[0], args.verbosity, 1,\
                   log_file = args.log_file)
            verify_file(args.fastr[0])
        main(args.fastr[0], args.min_length, args.max_length)
    output('Exiting filter__fastr.py', args.verbosity, 1,\
           log_file = args.log_file)
        
    sys.exit(0)
