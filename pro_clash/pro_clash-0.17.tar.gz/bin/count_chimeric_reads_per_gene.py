#!/usr/bin/env python

"""
Count how many reads overlap each gene in a gff file
"""

import sys
import argparse
from collections import defaultdict
import csv
import itertools

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
        description='Count reads per gene.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        'genes_gff',
        help='Name of gff file to count the reads per gene.')
    parser.add_argument(
        'reads_files', nargs='+',
        help='Reads files, output of map_chimeric_fragments.py')
    parser.add_argument(
        '-f', '--feature', default='exon',
        help='Name of features to count on the GTF file (column 2).')
    parser.add_argument(
        '-i', '--identifier', default='gene_id',
        help='Name of identifier to print (in column 8 of the GTF file).')
    parser.add_argument(
        '-o', '--overlap', type=int, default=5,
        help='Minimal overlap between gene and read.')



    settings = parser.parse_args(argv)

    return settings
def count_features(features, infile, overlap, length=25):
    """
    Count the number of reads for each feature
    Arguments:
    - `features`: Sict of features
    - `infile`: An open file, position and strand in cols 0-5
    - `overlap`: Minimal overlap between feature and read
    - `length`: Read length. added to first read and reduced from second
    """
    def update_counter(rfrom, rto, rstr, chrname,  fcounts):
        """
        Update the counters of features
        """
        in_feature = False
        rcounts = defaultdict(int)
        for fset in features[chrname+rstr][rfrom:rto]:
            for el in fset:
                rcounts[el] += 1
        for feat, counts in rcounts.items():
            if counts >= overlap:
                fcounts[feat] += 1
                in_feature = True
        if not in_feature:
            # test if antisense
            is_antis = False
            rev_str = '+'
            if rstr == '+':
                rev_str = '-'
            rev_counts = defaultdict(int)
            for fset in features[chrname+rev_str][rfrom:rto]:
                for el in fset:
                    rev_counts[el] += 1
            for feat, counts in rev_counts.items():
                if counts >= overlap:
                    is_antis = True
                    break
            if is_antis:
                fcounts['~~antisense'] += 1
            else:
                fcounts['~~intergenic'] += 1
                
    fcounts = defaultdict(int)
    for line in infile:
        try:
            r1_chrn, r1, str1, r2_chrn, r2, str2 = line.strip().split()[:6]
        except ValueError:
            sys.stderr.write('%s\t%s'%(infile.name, line))
        r1i = int(r1)-1 #0-based
        r2i = int(r2)-1
        r1_to = r1i+length
        if str1 == '-':
            r1_to = r1i+1
            r1i = r1_to-length
        r2_to = r2i + length
        if str2 == '+':
            r2_to = r2i+1
            r2i = r2_to - length
        update_counter(r1i, r1_to, str1, r1_chrn, fcounts)
        update_counter(r2i, r2_to, str2, r2_chrn, fcounts)
    return fcounts

def main(argv=None):
    settings = process_command_line(argv)
    try:
        pos_feat_list, all_features = pro_clash.read_gtf(
            open(settings.genes_gff), settings.feature, settings.identifier)
    except IOError:
        return 1
    lib_order = []
    all_counts = {}
    for r1_name in pro_clash.flat_list(settings.reads_files):
        sys.stderr.write('%s\n'%str(r1_name))
        lib_order.append(r1_name)
        all_counts[r1_name] = count_features(
            pos_feat_list, open(r1_name), settings.overlap, length=25)
    outt = csv.writer(sys.stdout, delimiter='\t')
    outt.writerow(['Gene name'] + lib_order)
    for g in sorted(list(all_features)):
        row_out = [g]
        for libn in lib_order:
            row_out.append(all_counts[libn][g])
        outt.writerow(row_out)
    # application code here, like:
    # run(settings, args)
    return 0        # success

if __name__ == '__main__':
    status = main()
    sys.exit(status)
