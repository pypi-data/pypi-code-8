#!/usr/bin/env python

'''obtains read depth data for a FASTA/Q file from a SAM file

Usage:

    generate_fastr.py [--log_file] [--verbose] [--version] [--verify]
                      <fastaq> <bsam> <fastr>

generate_fastr produce a FASTR file containing per base per entry
read depth data given a FASTA or FASTQ file and a SAM file.

FASTR Format:
    The FASTR Format is identical to the FASTA Format except the
bases are replaced by numbers representing the read depth of the
corresponding bases in the given FASTA file. Since read depth
numbers may contain more than one digit (e.g. a read depth of
10) so each number is separated by a hyphen. Additionally, the
">" at the beginning of each entry is replaced by a "+".
    The FASTR file also features file size reducing features.
First, this script does not include entries with read-depths
of only zeroes (no alignments anywhere in entry) though there
is nothing against doing this in general. Also, the FASTR file
can list read depth as:
    16-16-16 or 3x16
The later is compressed and thus reduces total file size.

FASTR Entry Example:

    +Corresponding FASTA or FASTQ header
    1-3x2-15x6-10-12x15

    or

    +Corresponding FASTA or FASTQ header
    1-2-2-2-6-6-6-6-6-6-6-6-6-6-6-6-6-6-6-10-15-15-15-15-15-15-15-15
    -15-15-15-15
'''

__version__ = '0.0.0.9'

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
    read depth to identigy regions of repeats and rewrites them
    as a multiplication. For example the following FASTR sequence:

    3-3-3-3-3-5-5-9-9-9-9-9-9

    is compressed to:

    5x3-2x5-6x9
    '''
    
    compressedSequence = ''
    lastRead = None
    readRepeats = 0
    count = 0
    for read in sequence:
        if read == lastRead:
            readRepeats += 1
        else:
            if readRepeats != 0:
                compressedSequence += str(readRepeats + 1) + 'x' +\
                                 str(lastRead) + '-'
                readRepeats = 0
            elif count != 0:
                compressedSequence += str(lastRead) + '-'
            lastRead = read
        count += 1
        if count == len(sequence):
            if readRepeats != 0:
                compressedSequence += str(readRepeats + 1) + 'x' +\
                                 str(lastRead) + '-'
            compressedSequence = compressedSequence[:-1]
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
            int(hit)
            decompressedSequence.append(int(hit))
        except ValueError:
            sep = hit.split('x')
            sep[1] = sep[1].replace('\n', '')
            for c in range(int(sep[0])):
                decompressedSequence.append(int(sep[1]))
    returnSequence = ''
    for base in decompressedSequence:
        returnSequence = returnSequence + str(base) + '-'
    returnSequence = returnSequence[:-1] # Remove trailing hyphen
    return returnSequence
    

def generate_fastr(fasta_q_file, depth_file,\
                   fasta_q_file_type, depth_file_type, fastr_file):
    '''Generates a FASTR file from the given FASTA/Q file and SAM file

    Input:
    
        fasta_q_file:
                A FASTA or FASTQ file containg the
                sequences that other sequences were
                mapped onto.
        
        depth_file:
                This depth file may be in SAM or BAM format.
                 
        fasta_q_file_type:
                ['fasta', 'fastq']

        depth_file_type:
                ['sam', 'bam']

    Output:
            A FASTR file containing per base read depth data for the given
            FASTA/Q file.

        generate_fastr generates list containing a "0" for each base
    in a given entry from the FASTA/Q file. It then uses pysam's pileup
    function to identify the read depth for a given base from a BAM files
    and changes the corresponding "0" in the aforementioned list. After each
    base's read depth is analyzed and corrected, the read depth list is
    compressed. If the compressed list only contains "0"s for read depths,
    then it is not written to the FASTR file, otherwise a FASTR entry is
    generated and writtein to the FASTR file.
    '''

    if fasta_q_file_type != 'fasta' and fasta_q_file_type != 'fastq':
        message = fasta_q_file_type + ' is not an acceptable file type.'\
                  + ' File type must be "fasta", or "fastq".'
        output(message, args.verbosity, 0, log_file = args.log_file,\
               fatal = True)
    if not fastr_file.endswith('.fastr'):
        fastr_file += '.fastr'
    if depth_file_type == 'sam':
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
    elif depth_file_type != 'bam':
        message = 'Must specify if alignment file is a SAM or a BAM'
        output(message, args.verbosity, 0, log_file = args.log_file,\
               fatal = True)
    header = ''
    sequenceLength = 0
    sequenceDepth = []
    readType = ''
    if sam_bam_file_type != 'bam':
        message = 'Must specify if alignment file is a SAM or BAM file.'
        output(message, args.verbosity, 0, log_file = args.log_file,\
               fatal = True)
    alignmentFile = pysam.Samfile(sam_bam_file, 'rb')
    for entry in entry_generator(fasta_q_file, fasta_q_file_type):
        header = entry[0][1:-1]
        output('Analyzing read depth for: ' + header, args.verbosity, 2,\
               log_file = args.log_file)
        sequenceId = header.split(' ')[0]
        sequenceLength = len(entry[1][:-1]) #Don't count \n in length
        sequenceDepth = [0 for base in range(sequenceLength)]
        for pileupColumn in alignmentFile.pileup(sequenceId):
            basePosition = pileupColumn.pos
            baseReadDepth = pileupColumn.n
            sequenceDepth[basePosition] = baseReadDepth
        output('Compressing sequence: ' + str(sequenceDepth), args.verbosity,\
               2, log_file = args.log_file)
        fastrSequence = compress_fastr(sequenceDepth)
        output('Compressed sequence: ' + fastrSequence, args.verbosity, 2,\
               log_file = args.log_file)
        sections = len(fastrSequence.split('-'))
        if sections > 1:
            message = 'Appending read depth for ' + header[1:-1] +\
                      ' to ' + fastr_file
            output(message, args.verbosity, 2,\
                   log_file = args.log_file)
            write_fastr(header, fastrSequence, fastr_file)
        else:
            message = header + ' has a read depth of zero for '+\
                          'each base. Not appending to ' + fastr_file
            output(message, args.verbosity, 2,\
                   log_file = args.log_file)
    alignmentFile.close

def write_fastr(sequence_ids, sequences, fastr_file, write_type = 'a'):
    '''Formats information for FASTR entries and writes them to a file

    Input:

        sequence_id:
                The ID of the entry to be written as a string for single
                entries or a list of strings for multiple entries.

        sequence:
                The sequence to be written as a string for single
                entries or a list of strings for multiple entries.

        fastr_file:
                The file for the entry to be written to.

        write_type:
                How the entry should be written to the fastr_file, e.g.
                "a" is for append and "w" is for write. Default is "a".

    Output:
            An entry is written to the fastr_file.

        For more information on FASTR file entries, type
    "metameta generate_fastr.py" with no further arguments.
    '''
    
    with open(fastr_file, write_type) as out_handle:
        # If the input is not a list, convert to a list
        try:
            assert type(sequence_ids) == list
        except AssertionError:
            sequence_ids = [sequence_ids]
            sequences = [sequences]
        for sequence_id, sequence in zip(sequence_ids, sequences):
            header = '+' + sequence_id + '\n'
            fastrSequence = sequence + '\n'
            out_handle.write(header + fastrSequence)
        
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
    parser.add_argument('bsam',
                        type = file_type,
                        default = None,
                        nargs = '?',
                        help = 'SAM or BAM file containing mapping' +\
                        'data for given FASTA/Q file')
    parser.add_argument('fastr',
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
         args.bsam == None or\
         args.fastr == None:
        message = 'Need to specify a FASTA/Q, B/SAM, and FASTR file.'
        output(message, args.verbosity, 0, fatal = True)
    else:
        if args.verify:
            output('Verifying: ' + args.fastaq[0], args.verbosity, 1,\
                   log_file = args.log_file)
            verify_file(args.fastaq[0])
            output('Verifying: ' + args.bsam[0], args.verbosity, 1,\
                   log_file = args.log_file)
            verify_file(args.bsam[0])
        output('Generating FASTR file: ' + args.fastr, args.verbosity, 1,\
               log_file = args.log_file)
        generate_fastr(args.fastaq[0], args.bsam[0],\
                       args.fastaq[1], args.bsam[1], args.fastr)
        output(args.fastr + '.fastr generated successfully.', args.verbosity,\
               2, log_file = args.log_file)
    output('Exiting generate__fastr.py', args.verbosity, 1,\
           log_file = args.log_file)
    
    sys.exit(0)
