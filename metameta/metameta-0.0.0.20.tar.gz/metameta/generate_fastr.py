#!/usr/bin/env python

'''obtains read depth data for a FASTA/Q file from a BAM file

Usage:

    generate_fastr.py <fastaq> <bam> <output>

Synopsis:

    reads alignment data from a BAM file to produce a FASTR file
    containing read depth data for the FASTA/Q file

Arguments:

    fastaq             FASTA or FASTQ file used as the mapping reference
    bam                BAM file containing alignment data
    output             Name of FASTR file containing read depth data to write
'''

__version__ = '0.0.0.10'

import argparse
from metameta_utilities import *
import pysam
import sys

def compress_fastr(sequence):
    '''Compresses a FASTR sequence

    Input:

        sequence:
                The FASTR sequence to compress as a list.

    Output:
            Returns the compressed FASTR sequence as a string.

        compress_fastr compares each read depth to the previous
    read depth to identify regions of repeats and rewrites them
    as a multiplication. For example the following FASTR sequence:

    3-3-3-3-3-5-5-9-9-9-9-9-9

    is compressed to:

    5x3-2x5-6x9
    '''
    
    compressedSequence = []
    lastRead = None
    readRepeats = 0
    for read in enumerate(sequence):
        if read[1] == lastRead:
            readRepeats += 1
        else:
            if readRepeats != 0:
                compressedSequence.append(str(readRepeats + 1) + 'x' +\
                                 str(lastRead))
                readRepeats = 0
            elif read[0] != 0:
                compressedSequence.append(str(lastRead))
            lastRead = read[1]
        if read[0] + 1 == len(sequence):
            if readRepeats != 0:
                compressedSequence.append(str(readRepeats + 1) + 'x' +\
                                 str(lastRead))
            else:
                compressedSequence.append(str(lastRead))
            compressedSequence = '-'.join(compressedSequence)
    return compressedSequence

def decompress_fastr(sequence):
    '''Decompresses a FASTR sequence

    Input:

        sequence:
                The FASTR sequence to decompress as a string.

    Output:
            Returns the decompressed FASTR sequence as a string.

        decompress_fastr splits a FASTR sequences by hyphens and
    then by "x" if possible. If split by "x" For example the following
    FASTR sequence:

    5x3-2x5-6x9

    is decompressed to:

    3-3-3-3-3-5-5-9-9-9-9-9-9
    '''

    depthSequence = sequence.split('-')
    decompressedSequence = []
    for base in depthSequence:
        try:
            int(base)
            decompressedSequence.append(int(base))
        except ValueError:
            sep = base.split('x')
            sep[1] = sep[1].rstrip('\n')
            decompressedSequence += [int(sep[1]) for i in range(int(sep[0]))]
    decompressedSequence = '-'.join([str(i) for i in decompressedSequence])
    return decompressedSequence

def write_fastr(sequence_ids, sequences, fastr_file, write_type = 'a'):
    '''Formats information for FASTR entries and writes them to a file

    Input:

        sequence_id:
                The ID of the entry to be written as a list of strings.

        sequence:
                The sequence to be written as a list of strings.

        fastr_file:
                The file for the entry to be written to.

        write_type:
                How the entry should be written to the fastr_file, e.g.
                "a" is for append and "w" is for write. Default is "a".

    Output:
            An entry is written to the fastr_file.
    '''
    
    with open(fastr_file, write_type) as out_handle:
        for sequence_id, sequence in zip(sequence_ids, sequences):
            header = '+' + sequence_id + '\n'
            fastrSequence = sequence + '\n'
            out_handle.write(header + fastrSequence)

def main():
    if args.fastaq[1] != 'fasta' and args.fastaq[1] != 'fastq':
        message = args.fastaq[1] + ' is not a FASTA or FASTQ file.'
        output(message, args.verbosity, 0, log_file = args.log_file,\
               fatal = True)
    if not fastr_file.endswith('.fastr'):
        fastr_file += '.fastr'
    if args.bam[1] == 'sam':
        message = 'Your alignment file is a SAM file. Please convert it\n'\
                  + 'into a BAM file, then sort and index it using the\n'\
                  + 'following commands:\n\n'\
                  + 'samtools view -h -S -b -F 4 -o <BAM file> <SAM file>\n'\
                  + 'samtools sort <BAM file> <sorted BAM file>\n'\
                  + 'samtools index <sorted BAM file>\n\n'\
                  + 'Then run this tool again with the BAM file.\n'\
                  + 'This allows generate_fastr to run with essentially\n'\
                  + 'zero memory and it runs roughly 20x faster than with\n'\
                  + 'a SAM file.'
        output(message, args.verbosity, 0, log_file = args.log_file,\
               fatal = True)
    elif args.bam[1] != 'bam':
        message = 'Must specify if alignment file is a SAM or a BAM'
        output(message, args.verbosity, 0, log_file = args.log_file,\
               fatal = True)
    header = ''
    sequenceLength = 0
    sequenceDepth = []
    readType = ''
    with pysam.Samfile(sam_bam_file, 'rb') as alignmentFile:
        for entry in entry_generator(args.fastaq[0]):
            # Don't include '+' in header
            header = entry[0][1:]
            output('Analyzing read depth for: ' + header, args.verbosity, 2,\
                   log_file = args.log_file)
            sequenceId = header.split(' ')[0]
            sequenceLength = len(entry[1])
            sequenceDepth = [0 for base in range(sequenceLength)]
            for pileupColumn in alignmentFile.pileup(sequenceId):
                basePosition = pileupColumn.pos
                baseReadDepth = pileupColumn.n
                sequenceDepth[basePosition] = baseReadDepth
            output('Compressing sequence: ' + str(sequenceDepth),\
                   args.verbosity, 2, log_file = args.log_file)
            fastrSequence = compress_fastr(sequenceDepth)
            output('Compressed sequence: ' + fastrSequence, args.verbosity, 2,\
                   log_file = args.log_file)
            sections = len(fastrSequence.split('-'))
            if sections > 1:
                message = 'Appending read depth for ' + header[1:-1] +\
                          ' to ' + fastr_file
                output(message, args.verbosity, 2,\
                       log_file = args.log_file)
                write_fastr([header], [fastrSequence], fastr_file)
            else:
                message = header + ' has a read depth of zero for '+\
                              'each base. Not appending to ' + fastr_file
                output(message, args.verbosity, 2,\
                       log_file = args.log_file)
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = __doc__,
                                        formatter_class = argparse.\
                                        RawDescriptionHelpFormatter)
    parser.add_argument('fastaq',
                        type = file_type,
                        default = None,
                        nargs = '?',
                        help = 'FASTA or FASTQ file to analyze the read' +\
                        ' depth of using the given SAM file')
    parser.add_argument('bam',
                        type = file_type,
                        default = None,
                        nargs = '?',
                        help = 'SAM or BAM file containing mapping' +\
                        'data for given FASTA/Q file')
    parser.add_argument('output',
                        default = None,
                        nargs = '?',
                        help = 'name of FASTR file to be written')
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
    elif args.fastaq == None:
        print(__doc__)
    elif args.fastaq == None or\
         args.bam == None or\
         args.output == None:
        message = 'Need to specify a FASTA/Q, B/SAM, and output file.'
        output(message, args.verbosity, 0, fatal = True)
    else:
        if args.verify:
            output('Verifying: ' + args.fastaq[0], args.verbosity, 1,\
                   log_file = args.log_file)
            verify_file(args.fastaq[0], log_file = args.log_file)
            output(args.fastaq[0] + ' is valid', args.verbosity, 1,\
                   log_file = args.log_file)
            output('Verifying: ' + args.bam[0], args.verbosity, 1,\
                   log_file = args.log_file)
            verify_file(args.bam[0] + ' is valid', log_file = args.log_file)
            output(args.bam[0], args.verbosity, 1,\
                   log_file = args.log_file)
        output('Generating FASTR file: ' + args.output, args.verbosity, 1,\
               log_file = args.log_file)
        generate_output(args.fastaq[0], args.bam[0],\
                       args.fastaq[1], args.bam[1], args.output)
        output(args.output + '.fastr generated successfully.', args.verbosity,\
               2, log_file = args.log_file)
    output('Exiting generate__fastr.py', args.verbosity, 1,\
           log_file = args.log_file)    
    sys.exit(0)
