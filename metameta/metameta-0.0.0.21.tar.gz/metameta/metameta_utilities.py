#!/usr/bin/env python

'''generic bioinformatic functions

Usage:

    metameta_utilities.py <functions>

<functions> will give the help for that each function
listed (multiple functions can be specified).

This file simply contains a number of generic bioinformatic
related functions useful to many programs in metameta. It
is meant to be imported by other scripts. Functions that
perform tasks represntative of another tool will be contained
in that tool, e.g. all functions for writing FASTR files
are in generate_fastr.py

Functions:
    entry_generator
    file_type
    filter_by_size
    gff_dict
    output
    same_gene
    verify_file
'''

__version__ = '0.0.0.13'

import argparse
import re
import string
import sys

def entry_generator(in_file, log_file = None,):
    '''Generates and returns entries for several bioinformatic file types

    Input:

        in_file:
                The FASTA, FASTQ, FASTR, GFF3, or SAM file to generate
                entries from

        log_file:
                A log file to write any output too. Default is None, which
                writes to stdout.

    Output:
            This function is a generator so it repeatedly yield
            entries. Each yielded entry is a list where each item
            is a different line of the entry. As such, SAM and GFF3 files
            have a single item, FASTA and FASTR files have two items, and
            FASTQ files have four items.
    '''

    entryParts = []
    acceptableFileTypes = ['fasta', 'fastq', 'fastr', 'gff3', 'sam']
    fileType = file_type(in_file)[1]
    if fileType not in acceptableFileTypes:
        strFileTypes = '\n'.join(acceptableFileTypes)
        message = fileType + ' is not an acceptable file type. Acceptable ' +\
                  ' file types are:\n' + strFileTypes + '\n'
        output(message, 1, 1, log_file = log_file, fatal = True)
    with open(in_file, 'rU') as in_handle:
        for line in in_handle:
            entryPartsLength = len(entryParts)
            if file_type == 'fasta' or file_type == 'fastr':
                if file_type == 'fasta':
                    startChar = '>'
                elif file_type = 'fastr':
                    startChar = '+'
                if line.startswith('@'):
                    message = in_file + ' may be a mixture of FASTA/R and '\
                              + 'FASTQ files. Suspect line follows: \n'\
                              + line + 'n\'
                    output(message, 1, 1, log_file = log_file, fatal = True)
                elif entryPartsLength == 0 and line.startswith(startChar):
                    entryParts.append(line.rstrip('\n'))
                elif line.startswith(startChar) and entryPartsLength == 2:
                    yield entryParts
                    entryParts = []
                    entryParts.append(line.rstrip('\n'))
                elif not line.startswith(startChar) and entryPartsLength != 0:
                    try:
                        entryParts[1] += line.rstrip('\n')
                    except IndexError:
                        entryParts.append(line.rstrip('\n'))
                else:
                    message = 'Unknown error with file.'
                    output(message, 1, 1, log_file = log_file, fatal = True)
            elif file_type == 'fastq':
                if line.startswith('>') and entryPartsLength < 3:
                    message = in_file + ' may be a mixture of FASTA and FASTQ'\
                              + ' files. Suspect line follows:\n'\
                              + line + '\n'
                    output(message, 1, 1, log_file = log_file, fatal = True)
                elif entryPartsLength == 0 and line.startswith('@'):
                    entryParts.append(line.rstrip('\n'))
                elif entryPartsLength == 1:
                    entryParts.append(line.rstrip('\n'))
                elif not line.startswith('+') and entryPartsLength == 2:
                    entryParts[1] += line.rstrip('\n')
                elif line.startswith('+') and entryPartsLength == 2:
                    entryParts.append(line.rstrip('\n'))
                elif entryPartsLength == 3:
                    entryParts.append(line.rstrip('\n'))
                elif len(entryParts[3]) > len(entryParts[1]):
                    wholeEntry = '\n'.join(entryParts)
                    message = 'Number of bases and quality scores do not '\
                              + 'match. The entry containing the error '\
                              + 'follows:\n' + wholeEntry + '\n'
                    output(message, 1, 1, log_file = log_file, fatal = True)
                elif entryPartsLength == 4 and len(entryParts[1]) !=\
                        len(entryParts[3]):
                    entryParts[3] += line.rstrip('\n')
                elif entryPartsLength == 4 and len(entryParts[1]) ==\
                        len(entryParts[3]):
                    yield entryParts
                    entryParts = []
                    entryParts.append(line.rstrip('\n'))
                else:
                    message = 'Unknown error with file.'
                    output(message, 1, 1, log_file = log_file, fatal = True)
            elif file_type == 'sam' or file_type == 'gff3':
                if file_type == 'sam':
                    starChar = '@'
                elif file_type == 'gff3':
                    starChar = '##'
                if not line.startswith(startChar):
                    parts = line.rstrip('\n').split('\t')
                    for part in parts:
                        entryParts.append(part)
                    yield entryParts
                    entryParts = []
        else: #yield entryParts at EOF so that last entry is not lost
            if entryParts != []:
                yield entryParts

def file_type(in_file, log_file = None):
    '''Reads the first line of the file and returns the file type

    Input:
            in_file:
                    A FASTA, FASTQ, GFF3, SAM, or BAM file

            log_file:
                    A log file to write any output too. Default is None, which
                    writes to stdout.

    Output:
            A tuple containing the input file name and the file type
            (in_file, ['bam', 'fasta', 'fastr', 'fastq', 'gff3', 'sam'])
    '''

    acceptableFileTypes = ['bam', 'fasta', 'fastq', 'fastr', 'gff3', 'sam']
    if fileType not in acceptableFileTypes:
        strFileTypes = '\n'.join(acceptableFileTypes)
        message = fileType + ' is not an acceptable file type. Acceptable ' +\
                  ' file types are:\n' + strFileTypes + '\n'
        output(message, 1, 1, log_file = log_file, fatal = True)
    with open(in_file, 'rU+') as in_handle:
        fileType = ''
        # Credit for following five lines:
        # http://code.activestate.com/recipes/
        # 173220-test-if-a-file-or-string-is-text-or-binary/
        charsToRemove = ''.join(map(chr, range(32 ,127)) + list('\n\r\t\b'))
        translationMap = string.maketrans('', '')
        firstBlock = in_handle.read(512)
        translatedBlock = firstBlock.translate(translationMap, charsToRemove)
        if float(len(translatedBlock))/float(len(firstBlock)) > 0.3:
            fileType = 'bam'
        elif firstBlock.startswith(('@HD', '@RG', '@SQ', '@PG', '@CO',)):
            fileType = 'sam'
        elif firstBlock.startswith('>'):
            fileType = 'fasta'
        elif firstBlock.startswith('+'):
            fileType = 'fastr'
        elif firstBlock.startswith('@'):
            fileType = 'fastq'
        elif firstBlock.startswith('##gff-version 3'):
            fileType = 'gff3'
        return (in_file, fileType)

def filter_by_size(unfiltered_list, tuple_pos = None, min_length = None,\
                   max_length = None, log_file = None):
    '''Filters a list of lists, or tuples, by size

    Input:

        unfiltered_list:
                A list of lists or tuples to be filtered by size.

        tuplePos:
                If unfiltered_list is a list of tuples, or there is a list,
                withing the each list, this argument
                specifies which item of the tuple contains the list
                to sort by length. Default is None.

        min_length:
                The minimum length a list must be to pass filtering.
                Default is None.

        max_length:
                The maximum length a list must be to pass filtering.
                Default is None.

        log_file:
                A log file to write output to. Defaults to None, which writes
                to stdout.

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
            message = str(listsToFilter[position]) + ' in '\
                      + str(unfiltered_list[position])\
                      + ' is less than the minimum length of '\
                      + str(min_length)
            output(message, args.verbosity, 2, log_file = log_file)
            shortLists.append(unfiltered_list[position])
        elif max_length != None and subLength > max_length:
            message = str(listsToFilter[position]) + ' in '\
                      + str(unfiltered_list[position])\
                      + ' is greater than the maximum length of '\
                      + str(max_length)
            output(message, args.verbosity, 2, log_file = log_file)
            longLists.append(unfiltered_list[position])
        else:
            message = str(listsToFilter[position]) + ' in '\
                      + str(unfiltered_list[position])\
                      + ' is within the length parameters: '\
                      + 'minimum length = ' + str(min_length)\
                      + ' and maximum length = ' + str(max_length)
            output(message, args.verbosity, 2, log_file = log_file)
            idealLists.append(unfiltered_list[position])
        position += 1
    return (shortLists, idealLists, longLists)

def gff_dict(gff_file):
    '''Reads a GFF file into a dictionary

    Input:

        gff_file:
                The GFF3 file to be read.

    Output:

            A dictionary where each key is a contig header. Each value is a
            list of tuples where each tuple contains nine items corresponds
            to the nine columns in a GFF3 entry.
    '''

    from collections import defaultdict
    annotations = defaultdict(list)
    for entry in entry_generator(gff_file, 'gff3'):
        annotations[entry[0]].append(tuple(entry))
    return annotations

def output(message, program_verbosity, message_verbosity, log_file = None,\
           fatal = False):
    '''Writes a verbosity dependant message to log file or STDOUT

    Input:

        message:
                A message to be output to a log file
                or STDOUT.

        program_verbosity:
                The verbosity setting of the program
                calling this function. This variable
                must be an integer.

        message_verbosity:
                The verbosity setting of the message
                to be written. This variable
                must be an integer.

        log_file:
                An optional log file to write the
                message to in place of STDOUT.

        fatal:
                Defaults to False, if True the
                program is terminated after the
                message is written.
        
    Output:
            The message from input, only output
            if message_verbosity is equal to or
            greather than program_verbosity.

        The message is written to STDOUT unless a log file is specified,
    then it is written to the log file. The message is only written if the
    message verbosity setting exceeds the verbosity setting of the
    progam. This offers a way to control the level of output such that
    a higher program verbosity results in more output. The fatality setting
    indicates whether or not to exit the program after the message is
    written. The log file and fatality settings default to None.
    '''
    
    if int(program_verbosity) >= int(message_verbosity):
        if fatal:
            fatalMessage = '\nAbove error is fatal. Exiting program.'
            message += fatalMessage
        if log_file == None:
            print(message)
        else:
            with open(log_file, 'a') as out_handle:
                out_handle.write(message + '\n')
        if fatal:
            sys.exit(1)

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

def verify_file(in_file, log_file = None):
    '''Checks a given file is valid

    Input:

        in_file:
                The file to verify.

        log_file:
                A log file to write any output too. Default is None, which
                writes to stdout.
    
    Output:
            A tuple with input file and file type.
            (input file, ['bam', 'fasta', 'fastr', 'fastq', 'gff3', 'sam'])

        This function determines whether a file is sent to file_type
    to determine how to evaluate the file. It then uses a file
    type dependant regular expression to analyze each entry in the file.
    If a file entry does not match the regular expression then the regular
    expression and entry are broken into parts so that the user is given
    a more precise error message.
        This function is fairly quick but may take some time on large
    files since it is iterating over every line of the file. Regular
    expressions do help to speed this process up. The tradeoff in speed
    is made up by a very picky verification that nearly garuntees that
    no file-related error will occur in the script using the file.
    '''

    fileRegex = {
        'fasta': r'^>.+\n[ACGTURYKMSWBDHVNX]+\n$',
        'fastq': r'^@.+\n[ACGTURYKMSWBDHVNX]+\n\+.*\n.+\n$',
        'fastr': r'^\+.+\n[\dx-]*\d\n$',
        'gff3': r'^[a-zA-Z0-9.:^*$@!+_?-|]+\t.+\t.+\t\d+\t\d+\t'\
                + r'\d+\.?\d*\t[+-.]\t[0-2]\t.*\n$',
        'sam': r'^[!-?A-~]{1,255}\t'\
               + r'([0-9]{1,4}|[0-5][0-9]{4}|'\
               + r'[0-9]{1,4}|[1-5][0-9]{4}|'\
               + r'6[0-4][0-9]{3}|65[0-4][0-9]{2}|'\
               + r'655[0-2][0-9]|6553[0-7])\t'\
               + r'\*|[!-()+-<>-~][!-~]*\t'\
               + r'([0-9]{1,9}|1[0-9]{9}|2(0[0-9]{8}|'\
               + r'1([0-3][0-9]{7}|4([0-6][0-9]{6}|'\
               + r'7([0-3][0-9]{5}|4([0-7][0-9]{4}|'\
               + r'8([0-2][0-9]{3}|3([0-5][0-9]{2}|'\
               + r'6([0-3][0-9]|4[0-7])))))))))\t'\
               + r'([0-9]{1,2}|1[0-9]{2}|'\
               + r'2[0-4][0-9]|25[0-5])\t'\
               + r'\*|([0-9]+[MIDNSHPX=])+\t'\
               + r'\*|=|[!-()+-<>-~][!-~]*\t'\
               + r'([0-9]{1,9}|1[0-9]{9}|2(0[0-9]{8}|'\
               + r'1([0-3][0-9]{7}|4([0-6][0-9]{6}|'\
               + r'7([0-3][0-9]{5}|4([0-7][0-9]{4}|'\
               + r'8([0-2][0-9]{3}|3([0-5][0-9]{2}|'\
               + r'6([0-3][0-9]|4[0-7])))))))))\t'\
               + r'-?([0-9]{1,9}|1[0-9]{9}|2(0[0-9]{8}|'\
               + r'1([0-3][0-9]{7}|4([0-6][0-9]{6}|'\
               + r'7([0-3][0-9]{5}|4([0-7][0-9]{4}|'\
               + r'8([0-2][0-9]{3}|3([0-5][0-9]{2}|'\
               + r'6([0-3][0-9]|4[0-7])))))))))\t'\
               + r'\*|[A-Za-z=.]+\t'\
               + r'[!-~]+\n$'
        }
    fileType = file_type(in_file)[1]
    if fileType == 'bam':
        return (in_file, fileType) #Don't verify BAM files
    else:
        regexString = re.compile(fileRegex[fileType])
    with open(in_file, 'rU') as in_handle:
        for entry in entry_generator(in_file, log_file):
            wholeEntry = '\n'.join(entry) + '\n'
            matches = re.findall(regexString, wholeEntry)
            if len(matches) != 1:
                if fileType == 'sam' or fileType == 'gff3':
                    splitRegex = regexString[1:-1].split(r'\t')
                    splitEntry = wholeEntry.split('\t')
                else:
                    splitRegex = regexString[1:-1].split(r'\n')
                    splitEntry = wholeEntry.split('\n')
                for regex, entry in zip(splitRegex[:-1], splitEntry[:-1]):
                    if not regex.startswith('^'):
                        regex = '^' + regex
                    if not regex.endswith('$'):
                        regex += '$'
                    splitMatches = re.findall(regex, entry)
                    if len(splitMatches) != 1:
                        message = 'The following line:\n\n' + entry + '\n'\
                                  + 'Does not match the regular expression:\n'\
                                  + '\n' + regex + '\n'\
                                  + 'See https://docs.python.org/3.4/'\
                                  + 'library/re.html for information '\
                                  + 'on how to interpret regular expressions.'\
                                  + '\nThe entire entry containing the error'\
                                  + ' follows:\n\n' + wholeEntry + '\n'
                        output(message, 1, 1, log_file = log_file,\
                               fatal = True)
    return (in_file, fileType)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = __doc__,
                                    formatter_class = argparse.\
                                    RawDescriptionHelpFormatter)
    parser.add_argument('functions',
                        default = None,
                        nargs = '*',
                        help = 'print function help')
    parser.add_argument('--version',
                        action = 'store_true',
                        help = 'prints tool version and exits')
    args = parser.parse_args()

    dict_functions = {
        'entry_generator': entry_generator,
        'file_type': file_type,
        'filter_by_size': filter_by_size,
        'gff_dict': gff_dict,
        'output': output,
        'same_gene': same_gene,
        'verify_file': verify_file,
        }
    
    if args.version:
        print(__version__)
        sys.exit(0)
    elif args.functions == None:
        print(__doc__)
        sys.exit(0)
    else:
        for function in args.functions:
            try:
                print(dict_functions[function].__doc__)
                print()
            except KeyError:
                print('\nThere is no such function: ' + function + '\n')
    sys.exit(0)
