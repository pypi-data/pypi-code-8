#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
CLC bio assembly file CAS, and the tabular format generated by `assembly_table
-n -s -p`
"""

import os.path as op
import sys
import logging

from Bio import SeqIO

from jcvi.formats.base import LineFile
from jcvi.formats.sizes import Sizes
from jcvi.apps.base import OptionParser, ActionDispatcher, sh, need_update


class CasTabLine (LineFile):
    """
    The table generate by command `assembly_table -n -s -p`
    from clcbio assembly cell
    """
    def __init__(self, line):
        args = line.split()
        self.readnum = args[0]  # usually integer or `-`
        self.readname = args[1]
        self.readlen = int(args[-10])
        # 0-based indexing
        self.readstart = int(args[-9])
        if self.readstart >= 0:
            self.readstart += 1

        self.readstop = int(args[-8])
        self.refnum = int(args[-7])

        self.refstart = int(args[-6])
        if self.refstart >= 0:
            self.refstart += 1

        self.refstop = int(args[-5])

        self.is_reversed = (int(args[-4]) == 1)
        self.strand = '-' if self.is_reversed else '+'

        self.nummatches = int(args[-3])
        self.is_paired = (int(args[-2]) == 1)
        self.score = int(args[-1])

    @property
    def bedline(self):
        return "\t".join(str(x) for x in (self.refnum,
            self.refstart - 1, self.refstop, self.readname,
            self.score, self.strand))


def main():

    actions = (
        ('txt', "convert CAS file to tabular output using `assembly_table`"),
        ('split', 'split CAS file into smaller CAS using `sub_assembly`'),
        ('bed', 'convert cas tabular output to bed format'),
        ('pairs', 'print paired-end reads of cas tabular output'),
        ('info', 'print the number of read mapping using `assembly_info`'),
            )
    p = ActionDispatcher(actions)
    p.dispatch(globals())


def info(args):
    """
    %prog info casfile <fastafile>

    Wraps around `assembly_info` and get the following block.

    General info:
    Read info:
    Coverage info:

    In particular, the read info will be reorganized so that it shows the
    percentage of unmapped, mapped, unique and multi-hit reads.

    When --coverage is used, the program expects a second fastafile to replace
    the contig IDs with real ones.

    RPKM = 10^9 x C / NL, which is really just simply C/N

    C = the number of mappable reads that felt onto the gene's exons
    N = total number of mappable reads in the experiment
    L = the sum of the exons in base pairs.
    """
    from jcvi.utils.cbook import percentage

    p = OptionParser(info.__doc__)
    p.add_option("--coverage", default=False, action="store_true",
            help="Generate coverage output, replacing IDs [default: %default]")
    opts, args = p.parse_args(args)

    if len(args) not in (1, 2):
        sys.exit(not p.print_help())

    casfile = args[0]
    pf = casfile.rsplit(".", 1)[0]

    if opts.coverage:
        assert len(args) == 2, "You need a fastafile when using --coverage"
        coveragefile = pf + ".coverage"
        fw = open(coveragefile, "w")

    infofile = pf + ".info"
    cmd = "assembly_info {0}".format(casfile)
    if not op.exists(infofile):
        sh(cmd, outfile=infofile)

    inreadblock = False
    incontigblock = False

    fp = open(infofile)
    row = fp.readline()
    while row:
        if row.startswith("Read info:"):
            inreadblock = True
        elif row.startswith("Contig info:"):
            incontigblock = True

        # Following looks like a hack, but to keep compatible between
        # CLC 3.20 and CLC 4.0 beta
        if inreadblock:
            atoms = row.split('s')

            last = atoms[-1].split()[0] if len(atoms) > 1 else "0"
            srow = row.strip()

            if srow.startswith("Reads"):
                reads = int(last)
            if srow.startswith("Unmapped") or srow.startswith("Unassembled"):
                unmapped = int(last)
            if srow.startswith("Mapped") or srow.startswith("Assembled"):
                mapped = int(last)
            if srow.startswith("Multi"):
                multihits = int(last)

            if row.startswith("Coverage info:"):
                # Print the Read info: block
                print "Read info:"
                assert mapped + unmapped == reads

                unique = mapped - multihits
                print
                print "Total reads: {0}".format(reads)
                print "Unmapped reads: {0}".format(percentage(unmapped, reads, False))
                print "Mapped reads: {0}".format(percentage(mapped, reads, False))
                print "Unique reads: {0}".format(percentage(unique, reads, False))
                print "Multi hit reads: {0}".\
                        format(percentage(multihits, reads, False))
                print
                inreadblock = False

        if incontigblock and opts.coverage:

            fastafile = args[1]
            s = Sizes(fastafile)
            while row:
                atoms = row.split()
                if len(atoms) == 4 and atoms[0][0] != "C":  # Contig
                    # Contig       Sites       Reads     Coverage
                    contig, sites, reads, coverage = atoms
                    contig = int(contig) - 1
                    size = s.sizes[contig]
                    contig = s.ctgs[contig]
                    assert size == int(sites)

                    # See formula above
                    rpkm = 1e9 * int(reads) / (size * mapped)
                    print >> fw, "\t".join((contig, sites, reads,
                        "{0:.1f}".format(rpkm)))

                row = fp.readline()

        row = fp.readline()


def txt(args):
    """
    %prog txt casfile

    convert binary CAS file to tabular output using CLC assembly_table
    """
    p = OptionParser(txt.__doc__)
    p.add_option("-m", dest="multi", default=False, action="store_true",
        help="report multi-matches [default: %default]")
    opts, args = p.parse_args(args)

    if len(args) != 1:
        sys.exit(p.print_help())

    casfile, = args
    txtfile = casfile.replace(".cas", ".txt")
    assert op.exists(casfile)

    cmd = "assembly_table -n -s -p "
    if opts.multi:
        cmd += "-m "
    cmd += casfile
    sh(cmd, outfile=txtfile)

    return txtfile


def split(args):
    """
    %prog split casfile 1 10

    split the binary casfile by using CLCbio `sub_assembly` program, the two
    numbers are starting and ending index for the `reference`; useful to split
    one big assembly per contig
    """
    p = OptionParser(split.__doc__)
    opts, args = p.parse_args(args)

    if len(args) != 3:
        sys.exit(p.print_help())

    casfile, start, end = args
    start = int(start)
    end = int(end)

    split_cmd = "sub_assembly -a {casfile} -o sa.{i}.cas -s {i} " + \
        "-e sa.{i}.pairs.fasta -f sa.{i}.fragments.fasta -g sa.{i}.ref.fasta"

    for i in range(start, end + 1):
        cmd = split_cmd.format(casfile=casfile, i=i)
        sh(cmd)


def check_txt(casfile):
    """
    Check to see if the casfile is already converted to txtfile with txt().
    """
    if casfile.endswith(".cas"):
        castabfile = casfile.replace(".cas", ".txt")
        if need_update(casfile, castabfile):
            castabfile = txt([casfile])
        else:
            logging.debug("File `{0}` found.".format(castabfile))
    else:
        castabfile = casfile

    return castabfile


def bed(args):
    """
    %prog bed casfile <fastafile>

    Convert the CAS or CASTAB format into bed format. If fastafile given, the
    sequential IDs in the casfile will be replaced by FASTA header.
    """
    p = OptionParser(bed.__doc__)
    opts, args = p.parse_args(args)

    nargs = len(args)
    if nargs not in (1, 2):
        sys.exit(not p.print_help())

    hasfastafile = (nargs == 2)
    casfile = args[0]
    castabfile = check_txt(casfile)

    if hasfastafile:
        fastafile = args[1]
        refnames = [rec.id for rec in SeqIO.parse(fastafile, "fasta")]

    fp = open(castabfile)
    bedfile = castabfile.rsplit(".", 1)[0] + ".bed"

    if need_update(castabfile, bedfile):
        fw = open(bedfile, "w")
        for row in fp:
            b = CasTabLine(row)
            if b.readstart == -1:
                continue
            if hasfastafile:
                b.refnum = refnames[b.refnum]
            print >> fw, b.bedline

        logging.debug("File written to `{0}`.".format(bedfile))
    else:
        logging.debug("File `{0}` up to date. Computation skipped.".\
                      format(bedfile))

    return bedfile


def pairs(args):
    """
    See __doc__ for OptionParser.set_pairs().
    """
    import jcvi.formats.bed

    p = OptionParser(pairs.__doc__)
    p.set_pairs()
    opts, targs = p.parse_args(args)

    if len(targs) != 1:
        sys.exit(not p.print_help())

    casfile, = targs
    bedfile = bed([casfile])
    args[args.index(casfile)] = bedfile

    return jcvi.formats.bed.pairs(args)


if __name__ == '__main__':
    main()
