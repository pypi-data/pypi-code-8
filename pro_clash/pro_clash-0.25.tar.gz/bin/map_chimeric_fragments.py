
#!/usr/bin/env python

"""
After a library is mapped to the genome (using map_single_fragments.py or any
other mapper), the bam file is screened for reads that weren't mapped to the
genome or weren't concise and try to map wach of the ends to a different
location. This script report the reads that are chimeric in a table of the
format:
chr1   position1    strand1    chr2   position2    strand2    read_name

where the position1 is the first position of the first read and position2 is
the last position of read2.
The input is a list of bam files, the output is always one list. The list can
be separated afterwards according to read names.
"""

import sys
import argparse
import pysam

import pro_clash

def process_command_line(argv):
    """
    Return a 2-tuple: (settings object, args list).
    `argv` is a list of arguments, or `None` for ``sys.argv[1:]``.
    """
    if argv is None:
        argv = sys.argv[1:]

    # initialize the parser object, replace the description
    parser = argparse.ArgumentParser(
        description='Map unmapped reads as chimeric fragments',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        'genome_fasta',
        help='Name of genome fasta file. The file must be indexed using'
        'bwa index command prior to this run.')
    parser.add_argument(
        'bamfiles', nargs='+', action='append',
        help='One or more bam files.')
    parser.add_argument(
        '-r', '--reverse_complement', default=False,
        action='store_true',
        help='Treat the reads as reverse complement. This means that the first'
        " read is actually the 3' end of the fragment. Use this when using "
        "Jonathan Livny's protocol for library construction")
    parser.add_argument(
        '-t', '--transcripts',
        help='A gff file od transcripts. If given, screen reads that might'
        ' reside from the same transcript. Very useful for screening ribosomal'
        ' RNAs. Otherwise use only the size limit.')
    parser.add_argument(
        '-s', '--distance', type=int, default=1000,
        help='Maximal distance between concordant reads. If they are generated'
        ' from the same strand but larger than this distance they will be'
        ' considered as chimeric.')
    parser.add_argument(
        '-d', '--dirout', default='.',
        help='Output directory, default is this directory.')
    parser.add_argument(
        '--keep_circular', default=False, action='store_true',
        help='Remove reads that are probably a result of circular RNAs by'
        ' default. If the reads are close but in opposite order they will be'
        ' removed unless this argument is set.')
    parser.add_argument(
        '-l', '--length', type=int, default=25,
        help='Length of sequence to map. Take the ends of the fragment and map'
        ' each to the genome. The length of the region will be this length.')
    parser.add_argument(
        '--max_mismatches', type=int, default=3,
        help='Find alignment allowing this number of mismatches. If there are '
        'more than one match with this number of mismatches the read will be'
        ' treated as if it might match all of them and if there is one '
        'scenario in which the two ends are concordant it will be removed.')
    parser.add_argument(
        '--allowed_mismatches', type=int, default=1,
        help='This number of mismatches is allowed between the a match and '
        'the genome. If there are mapped reads with less than --max_mismatches'
        ' mismatches but more than this number the read will be ignored.')
    parser.add_argument(
        '--maxG', type=float, default=0.8,
        help='If a read has more than this fraction of Gs remove this read'
        'from the screen. This is due to nextseq technology wcich puts G '
        'where there is no signal, the poly G might just be noise.'
        ' When using other sequencing technologies set to 1.')
    parser.add_argument(
        '-p', '--processors', type=int, default=8,
        help='Number of processors to be used by bwa aln.')
    parser.add_argument(
        '--bwa_exec', default='bwa',
        help='bwa command')
    parser.add_argument(
        '-S', '--samtools_cmd', default='samtools',
        help='Samtools executable.')
    parser.add_argument(
        '--params_aln', default='-k 2 -l 6 -N -M 0',
        help='Additional parameters for aln function of bwa.')
    parser.add_argument(
        '--samse_params', default='-n 1000',
        help='Additional parameters for samse function of bwa.')
    settings = parser.parse_args(argv)

    return settings

def main(argv=None):
    settings = process_command_line(argv)
    # Read the transcripts if given
    if settings.transcripts:
        trans_dict = pro_clash.read_transcripts(settings.transcripts)
    else:
        trans_dict = None
    # Get the ends of the reads from the bam files
#    sys.stderr.write('%s\n'%str(settings.bamfiles))
    for bf in pro_clash.flat_list(settings.bamfiles):
        bfin = pysam.Samfile(bf)
        outhead = bf.rsplit('.', 1)[0]
        libname = outhead.rsplit('/',1)[-1]
        fsq1name = "%s/%s_ends_1.fastq"%(settings.dirout, libname)
        fsq1 = open(fsq1name, 'w')
        fsq2name = "%s/%s_ends_2.fastq"%(settings.dirout, libname)
        fsq2 = open(fsq2name, 'w')
        pro_clash.get_unmapped_reads(
            bfin, fsq1, fsq2, settings.length, settings.maxG,
            rev=settings.reverse_complement)
        # Map the fastq files to the genome
        reads_in = []
        for fqname in (fsq1name, fsq2name):
            bamheadname = fqname.rsplit('.',1)[0].rsplit('/',1)[-1]
            bamname = pro_clash.run_bwa(
                settings.bwa_exec, fqname, None,
                settings.dirout, bamheadname, settings.max_mismatches,
                settings.genome_fasta, settings.params_aln,
                '', settings.samse_params,
                settings.samtools_cmd, processors=settings.processors)
            bamin = pysam.Samfile(bamname)
            reads_in.append(pro_clash.read_bam_file(
                    bamin, bamin.references, settings.allowed_mismatches))
        pro_clash.write_reads_table(
            sys.stdout, reads_in[0], reads_in[1], bfin.references,
            settings.distance, not settings.keep_circular,
            trans_dict)
    return 0        # success

if __name__ == '__main__':
    status = main()
    sys.exit(status)
