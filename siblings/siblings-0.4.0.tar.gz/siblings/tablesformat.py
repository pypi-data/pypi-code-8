import tables as tb


class Matches(tb.IsDescription):
    EntryNr1 = tb.UInt32Col(pos=1)
    EntryNr2 = tb.UInt32Col(pos=2)
    Score = tb.Float32Col(pos=3)
    PamDistance = tb.Float32Col(pos=4)
    Start1 = tb.UInt16Col(pos=5)
    End1 = tb.UInt16Col(pos=6)
    Start2 = tb.UInt16Col(pos=7)
    End2 = tb.UInt16Col(pos=8)
    PamVariance = tb.Float32Col(pos=9)
    LogEValue = tb.Float32Col(pos=10)
    PIdent = tb.Float32Col(pos=11)
    Global_Score = tb.Float32Col(pos=12)
    Global_PamDistance = tb.Float32Col(pos=13)
    Global_PamVariance = tb.Float32Col(pos=14)
    Global_PIdent = tb.Float32Col(pos=15)


class XRef(tb.IsDescription):
    NCBITaxonId = tb.UInt32Col(pos=1)
    EntryNr = tb.UInt32Col(pos=2)
    XRefSource = tb.EnumCol(
        tb.Enum(['UniProtKB/SwissProt', 'UniProtKB/TrEMBL', 'n/a', 'EMBL',
                 'Ensembl Gene', 'Ensembl Transcript', 'Ensembl Protein',
                 'RefSeq', 'EntrezGene', 'GI', 'WikiGene', 'IPI',
                 'Description', 'SourceID', 'SourceAC']),
        'n/a', base='uint8', pos=3)
    XRefId = tb.StringCol(30, pos=4)


class Genome(tb.IsDescription):
    NCBITaxonId = tb.UInt32Col(pos=1)
    UniProtSpeciesCode = tb.StringCol(5, pos=2)
    SciName = tb.StringCol(150, pos=3)
    TotEntries = tb.UInt32Col(pos=4)
    DBRelease = tb.StringCol(70, pos=5)


class Protein(tb.IsDescription):
    EntryNr = tb.UInt32Col(pos=1)
    SequenceBufferOffset = tb.UInt32Col(pos=2)
    SequenceBufferLength = tb.UInt32Col(pos=3)
    DNABufferOffset = tb.UInt32Col(pos=4)
    DNABufferLength = tb.UInt32Col(pos=5)
    CanonicalId = tb.StringCol(20, pos=6, dflt=b'')


class XRefGenomes(tb.IsDescription):
    NCBITaxonId = tb.UInt32Col(pos=1)
    XRefSource = tb.StringCol(10, pos=2)
    XRefId = tb.StringCol(15, pos=3)


class JobsToExecute(tb.IsDescription):
    JobId = tb.StringCol(32, pos=1)
    Genome1 = tb.UInt32Col(pos=2)
    Genome2 = tb.UInt32Col(pos=2)
    Range1 = tb.UInt32Col(pos=3, shape=(2,))
    Range2 = tb.UInt32Col(pos=4, shape=(2,))
    Submit_time = tb.Float64Col(pos=5, dflt=0)
    ErrorCount = tb.UInt8Col(pos=6, dflt=0)


class Timings(tb.IsDescription):
    User = tb.StringCol(20, pos=1)
    Host = tb.StringCol(20, pos=2)
    Total_nr_jobs = tb.UIntCol(pos=3)
    Total_time = tb.Float32Col(pos=4)
    Total_time2 = tb.Float32Col(pos=5)


class PairStatus(tb.IsDescription):
    Genome1 = tb.UInt32Col(pos=1)
    Genome2 = tb.UInt32Col(pos=2)
    Status = tb.EnumCol(tb.Enum(['QUEUED', 'NEW', 'COMPUTED', 'VERIFIED']),
                        pos=3, base='uint8', dflt='NEW')


class UniProtTaxonomy(tb.IsDescription):
    pass
