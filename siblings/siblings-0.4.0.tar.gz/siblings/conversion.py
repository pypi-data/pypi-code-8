from __future__ import print_function, absolute_import

import Bio.SeqIO
import Bio.SeqRecord
from Bio.Seq import UnknownSeq
from Bio.Alphabet import IUPAC
import gzip
import re
import csv
import collections
import json

class GenomeJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, GenomeConverter):
            return {'NCBITaxonId': o.NCBITaxonId,
                    'UniProtSpeciesCode': o.UniProtSpeciesCode,
                    'SciName': o.SciName,
                    'Release': o.Release,
                    'Entries': o.Entries}
        return json.JSONEncoder.default(self, o)

class GenomeConverter(object):
    def __init__(self):
        self.NCBITaxonId = None
        self.UniProtSpeciesCode = None
        self.SciName = None
        self.Release = None
        self.Entries = []
        self.processed = False

    def parse(self):
        raise NotImplementedError()

    def to_json(self):
        if not self.processed:
            self.parse()
        return json.dumps(self, cls=GenomeJSONEncoder)


class ReferenceSpeciesConverter(GenomeConverter):
    def __init__(self, tax, fastafile, dnafile, xreffile, add_fastafile=None):
        super(ReferenceSpeciesConverter, self).__init__()
        self.NCBITaxonId = tax
        self.fasta = fastafile
        self.dna = dnafile
        self.xref = xreffile
        self.iso = add_fastafile
        self.os_regex = re.compile(r'OS=(?P<sciname>[^=]*)\s+\w+=')

    def _id_from_fasta_header(self, rec):
        return rec.name.split('|')[1]

    def _get_cDNA_dict(self, fn):
        with gzip.GzipFile(fn) as fh:
            dna = Bio.SeqIO.to_dict(Bio.SeqIO.parse(fh, 'fasta'),
                            key_function=self._id_from_fasta_header)
        return dna

    def _get_xref_dict(self, fn):
        with gzip.GzipFile(fn) as fh:
            reader = csv.reader(fh, delimiter='\t')
            xrefs = collections.defaultdict(list)
            for row in reader:
                xrefs[row[0]].append(row[1:])
        return xrefs

    def _set_UniProtSpeciesCode_if_found(self, rec):
        name_parts = rec.name.split('|')
        if len(name_parts) > 2 and name_parts[2].index('_')>0:
            self.UniProtSpeciesCode = name_parts[2][name_parts[2].index('_')+1:]

    def _set_SciName_if_found(self, rec):
        match = self.os_regex.search(rec.description)
        if match:
            self.SciName = match.group('sciname')

    def parse(self):
        dna = self._get_cDNA_dict(self.dna)
        xrefs = self._get_xref_dict(self.xref)

        for fname in (self.fasta, self.iso):
            if fname is None:
                continue
            with gzip.GzipFile(fname) as fh:
                for rec in Bio.SeqIO.parse(fh, 'fasta'):
                    key = self._id_from_fasta_header(rec)
                    try:
                        cDNA = dna[key]
                    except KeyError:
                        cDNA = Bio.SeqRecord.SeqRecord(UnknownSeq(3*(len(rec)+1), IUPAC.ambiguous_dna),
                                                       id=key)
                    self.Entries.append({'Id': key, 'Sequence': str(rec.seq),
                                         'cDNA': str(cDNA.seq), 'xrefs': xrefs[key]})
                    if self.UniProtSpeciesCode is None:
                        self._set_UniProtSpeciesCode_if_found(rec)
                    if self.SciName is None:
                        self._set_SciName_if_found(rec)
        self.processed = True

