import json
import re
import tables as tb
import numpy as np
import os
import subprocess
import sys
import uuid
import errno
import multiprocessing as mp
import Queue
import itertools
import gzip
import time

from .tablesformat import *
from .common import package_logger

# maximum size of a matches file before
# creating a new one. TODO: parameter file
MAX_MATCH_FILE_SIZE_SOFT = pow(2, 30) + pow(2, 29)


class DarwinException(Exception):
    pass


class ImportException(Exception):
    pass


class MatchExporter(object):
    def __init__(self, taxClass, rootOfHDF5Files, logger=None):
        self.logger = logger if logger is not None else package_logger
        self.taxClass = taxClass
        self.rootOfHDF5Files = os.path.abspath(
            os.path.normpath(os.path.expanduser(rootOfHDF5Files)))
        if not os.path.exists(self.rootOfHDF5Files):
            os.makedirs(self.rootOfHDF5Files)
        fn = os.path.join(self.rootOfHDF5Files, "%s.h5" % (taxClass))
        self._compr = tb.Filters(complevel=5, complib='zlib', fletcher32=True)
        # self._compr = tb.Filters(complevel=5, complib='blosc', fletcher32=True)
        self._masterfile = tb.open_file(fn, mode='a', filters=self._compr)
        self.logger.info("writing to %s, options %s" % (fn, str(self._compr)))

    def getGenomes(self):
        raise NotImplementedError("concrete classes should implement this method")

    def _getSequence(self, g, nr):
        raise NotImplementedError("concrete classes should implement this method")

    def _getDNA(self, g, nr):
        raise NotImplementedError("concrete classes should implement this method")

    def _getXRefs(self, g, nr):
        raise NotImplementedError("concrete classes should implement this method")

    def _getGenomeMetaData(self, g):
        """retreive the all the meta information about a genome and return a
        dictionary with the values."""
        raise NotImplementedError("concrete classes should implement this method")

    def _finishedGenome(self, g):
        """this function is called after a genome has been successfully added
        to the pytables"""
        pass

    def _finishedMatches(self, g1, g2):
        pass

    def _genomeIsImported(self, g):
        GSnode = self._masterfile.get_node('/Genomes', 'Summaries')
        return len(list(GSnode.where('NCBITaxonId==%d' % (g)))) > 0

    def getAndStoreGenomeData(self):
        genomeFilePath = os.path.join(self.rootOfHDF5Files, "genomes")
        if not os.path.exists(genomeFilePath):
            os.makedirs(genomeFilePath)
        try:
            gGroup = self._masterfile.get_node('/Genomes')
        except tb.NoSuchNodeError:
            gGroup = self._masterfile.createGroup('/', 'Genomes')

        try:
            GSumTab = self._masterfile.get_node(gGroup, 'Summaries')
        except tb.NoSuchNodeError:
            GSumTab = self._masterfile.createTable(gGroup, 'Summaries',
                                                   Genome, expectedrows=len(self.getGenomes()))

        try:
            XRefTab = self._masterfile.get_node(gGroup, 'XRefs')
        except tb.NoSuchNodeError:
            XRefTab = self._masterfile.createTable(gGroup, 'XRefs', XRef)

        GSumRow = GSumTab.row
        XRefRow = XRefTab.row
        xrefSourceEnum = XRefTab.get_enum('XRefSource');
        for g in self.getGenomes():
            if self._genomeIsImported(g):
                sys.stderr.write('already imported %s\n' % (g))
                continue

            sys.stderr.write('processing %s\n' % (g))
            self.__createGenomeDb(g, genomeFilePath)
            metaInfo = self._getGenomeMetaData(g)
            GSumRow['UniProtSpeciesCode'] = metaInfo['5LETTERNAME']
            GSumRow['NCBITaxonId'] = metaInfo['TAXONID']
            GSumRow['SciName'] = metaInfo['SCINAME']
            GSumRow['TotEntries'] = metaInfo['TotEntries']
            GSumRow['DBRelease'] = metaInfo['DBRELEASE']
            GSumRow.append()
            for xref in self._getXRefs(g):
                XRefRow['NCBITaxonId'] = xref[0]
                XRefRow['EntryNr'] = xref[1]
                XRefRow['XRefSource'] = xrefSourceEnum[xref[2]]
                XRefRow['XRefId'] = xref[3]
                XRefRow.append()
            XRefTab.flush()
            GSumTab.flush()
            self._finishedGenome(g)

    def __createGenomeDb(self, g, genomeFilePath):

        metaInfo = self._getGenomeMetaData(g)
        genomeFileName = os.path.join(genomeFilePath, "%s.h5" % (g))
        gFile = tb.open_file(genomeFileName, mode='w', filters=self._compr)
        grpPath = "/Proteins"
        grpDir, grpName = os.path.split(grpPath)
        grpNode = gFile.create_group(grpDir, grpName,
                                     "Data about Proteins in %s" % (g))
        protTab = gFile.create_table(grpNode, "Entries", Protein,
                                     expectedrows=metaInfo["TotEntries"])
        seqArr = gFile.create_earray(grpNode, "SequenceBuffer",
                                     tb.StringAtom(1), (0,), "concatenated protein sequences",
                                     expectedrows=metaInfo["TotAA"])
        dnaArr = gFile.create_earray(grpNode, "DNABuffer", tb.StringAtom(1),
                                     (0,), "concatenated cdna sequences",
                                     expectedrows=3 * metaInfo["TotAA"] + metaInfo["TotEntries"])
        for eNr in range(metaInfo["TotEntries"]):
            protRow = protTab.row
            seq = self._getSequence(g, eNr + 1)
            dna = self._getDNA(g, eNr + 1)
            # write protein info in table
            protRow['EntryNr'] = eNr + 1
            protRow['SequenceBufferOffset'] = seqArr.nrows
            protRow['SequenceBufferLength'] = len(seq)
            protRow['DNABufferOffset'] = dnaArr.nrows
            protRow['DNABufferLength'] = len(dna)
            protRow.append()
            # add sequences to buffers
            seqArr.append(np.ndarray((len(seq),), buffer=seq.encode('ascii'), dtype=tb.StringAtom(1)))
            dnaArr.append(np.ndarray((len(dna),), buffer=dna.encode('ascii'), dtype=tb.StringAtom(1)))
        protTab.flush()
        seqArr.flush()
        dnaArr.flush()
        relPathToGrpNode = str(self._rel_path_to_master_file(genomeFileName) + ":" + grpPath)
        self._masterfile.create_external_link("/Genomes", "tax%d" % (g), relPathToGrpNode)
        gFile.close()

    def _rel_path_to_master_file(self, path):
        """returns the relative path with respect to the master hdf5 file"""
        return os.path.relpath(path, self.rootOfHDF5Files)

    def getAndStoreMatchData(self):
        """This function extracts the all the matches between the set of genomes
        defined by its class and stores them in individal hdf5 files which are
        linked into the main file."""
        self._setup_matches_node_structure()
        matches_filepath = os.path.join(self.rootOfHDF5Files, 'matches')
        if not os.path.exists(matches_filepath):
            os.mkdir(matches_filepath)

        nr_workers = mp.cpu_count()
        job_queue, result_queue = mp.Queue(1024), mp.Queue()
        jobs = list(self.iter_nonexisting_genomepairs())
        mp.Process(target=queue_feeder, args=(job_queue, jobs, nr_workers,)).start()
        for i in xrange(nr_workers):
            DarwinMatchImportWorker(self.rootOfHDF5Files,
                                    os.path.join(self.rootOfHDF5Files, 'matches'),
                                    self._compr, job_queue, result_queue).start()

        cnt_end = 0
        while cnt_end < nr_workers:
            self.logger.debug('result_queue size: %d' % (result_queue.qsize()))
            res = result_queue.get()
            if res is None:
                cnt_end += 1
            else:
                self._store_matches_link(*res)

    def _setup_matches_node_structure(self):
        """function to create a /Matches/taxXXXX structure (for each
        genome) in the masterfile. If the structure already exists,
        no error will be reported."""
        try:
            mGroup = self._masterfile.get_node('/Matches')
        except tb.NoSuchNodeError:
            mGroup = self._masterfile.createGroup('/', 'Matches')
        for g in self.getGenomes():
            nodename = 'tax%d' % (g)
            if not nodename in mGroup:
                self._masterfile.createGroup(mGroup, nodename)

    def iter_nonexisting_genomepairs(self):
        genomes = self.getGenomes()
        for g1, g2 in itertools.combinations_with_replacement(genomes, 2):
            nodeName = '/Matches/tax%d/tax%d' % (g1, g2)
            if nodeName in self._masterfile:
                continue
            i, j = map(genomes.index, (g1, g2))
            yield g1, g2

    def _store_matches_link(self, g1, g2, link_dest):
        self._masterfile.createExternalLink("/Matches/tax%d" % (g1),
                                            "tax%d" % (g2), link_dest)
        if g1 != g2:
            self._masterfile.createExternalLink("/Matches/tax%d" % (g2),
                                                "tax%d" % (g1), link_dest)
        self.logger.info('Master: stored link to matches for (%d vs %d)' % (g1, g2))

    def close(self):
        self._masterfile.close()


class DarwinFilesExporter(MatchExporter):
    def __init__(self, taxClass, rootOfHDF5Files, logger=None):
        super(DarwinFilesExporter, self).__init__(taxClass, rootOfHDF5Files, logger)
        data = callDarwinExport("GetGenomeSummary('%s')" % (taxClass))
        if len(data['genomes']) < 2:
            raise ImportException("Class '%s' contains too few genomes" % (taxClass))
        self.__genomes = data["genomes"]
        self.__summaries = data["summaries"]
        self.__tax2five = dict([(int(data["summaries"][g]['TAXONID']), g)
                                for g in data["genomes"]])
        self.__seq = dict()
        self.__dna = dict()
        self.__xref = dict()

    def __mapGenomeId(self, taxid):
        return self.__tax2five[taxid]

    def iter_nonexisting_genomepairs(self):
        pairs_gen = super(DarwinFilesExporter, self).iter_nonexisting_genomepairs()
        for t1, t2 in pairs_gen:
            g1, g2 = map(self.__mapGenomeId, (t1, t2,))
            if self.__genomeIsLarger(g1, g2):
                g1, g2 = g2, g1
                t1, t2 = t2, t1
            yield t1, g1, t2, g2

    def getGenomes(self):
        return list(self.__tax2five.keys())

    def __extractSequencesFromDarwinGenomeDB(self, t):
        g = self.__mapGenomeId(t)
        data = callDarwinExport("LoadSequences('%s')" % (g))
        self.__seq[g] = data["seq"]
        self.__dna[g] = data["dna"]
        self.__xref[g] = data["xref"]
        assert len(data['seq']) == self.__summaries[g]['TotEntries'], "Length differ: %d != %d" % (
            len(data['seq']), self.__summaries[g]['TotEntries'])


    def _getSequence(self, t, nr):
        g = self.__mapGenomeId(t)
        if not g in self.__seq:
            self.__extractSequencesFromDarwinGenomeDB(t)
        return self.__seq[g][nr - 1]

    def _getDNA(self, t, nr):
        g = self.__mapGenomeId(t)
        if not g in self.__dna:
            self.__extractSequencesFromDarwinGenomeDB(t)
        return self.__dna[g][nr - 1]

    def _getXRefs(self, t, nr=None):
        g = self.__mapGenomeId(t)
        if not g in self.__xref:
            self.__extractSequencesFromDarwinGenomeDB(t)
        return [(t, xref[0], xref[1], xref[2]) for xref in self.__xref[g] if nr is None or xref[0] == nr]


    def _getGenomeMetaData(self, t):
        g = self.__mapGenomeId(t)
        return self.__summaries[g]

    def __genomeIsLarger(self, g1, g2):
        """determine which of the two genomes is larger. this is a helper
        method to determine the genome order in the darwin matches structure."""
        n1 = self.__summaries[g1]['TotEntries']
        n2 = self.__summaries[g2]['TotEntries']
        return (n1 > n2 or (n1 == n2 and g1 > g2))

    def _finishedGenome(self, t):
        """remove the no longer used data to free memory again"""
        g = self.__mapGenomeId(t)
        self.__seq.pop(g, None)
        self.__dna.pop(g, None)
        self.__xref.pop(g, None)


class DarwinMatchImportWorker(mp.Process):
    def __init__(self, dataroot_path, matches_path, compr, task_queue, done_queue, logger=None):
        super(DarwinMatchImportWorker, self).__init__()
        self.task_queue = task_queue
        self.done_queue = done_queue
        self.dataroot_path = dataroot_path
        self.matches_filepath = matches_path
        self._compr = compr
        self._last_match_file = None
        self.logger = logger if logger is not None else package_logger

    def run(self):
        for t1, g1, t2, g2 in iter(self.task_queue.get, None):
            matchesdata = self.load_matches(t1, g1, t2, g2)
            self.logger.debug('%s: result_queue (w) size: %d' % (self.name, self.done_queue.qsize()))
            self.done_queue.put(self._createMatchesDb(matchesdata))
            self.logger.debug('%s: job_queue (r) size: %d' % (self.name, self.task_queue.qsize()))
        self.done_queue.put(None)
        if not self._last_match_file is None:
            self._last_match_file.close()

    def load_matches(self, t1, g1, t2, g2):
        try:
            jsonPath = os.path.join(os.getenv('SIBLING_JSON_PATH', ''), g1, g2 + ".json.gz")
            with gzip.open(jsonPath, 'r') as json_fd:
                result = json.load(json_fd)
        except IOError:
            result = callDarwinExport("ReadAllAll('%s','%s')" % (g1, g2))
        result['g1'] = t1
        result['g2'] = t2
        return result

    def _createMatchesDb(self, matchesdata):
        mFile = self._get_maches_filehandle()
        g1 = matchesdata['g1']
        g2 = matchesdata['g2']
        tabDir, tabName = '/tax%d' % (g1), 'tax%d' % (g2)
        mtab = mFile.createTable(tabDir, tabName, Matches,
                                 "Matches between %d and %d" % (g1, g2),
                                 expectedrows=matchesdata['cnt'],
                                 createparents=True)
        # fix a problem in the exported data, e.g. %identiy is not percent.
        # trim precision to safe space
        matches = np.rec.array(matchesdata['matches'], dtype=mtab.dtype)
        for col in ('PIdent', 'Global_PIdent',):
            matches[col] = np.around(100 * matches[col], 3)
        mtab.append(matches);
        mtab.set_attr('g1', g1)
        mtab.set_attr('g2', g2)
        mtab.flush()
        self.logger.info("%s: compression ratio of %s: %.3f%%" % (self.name,
                                                                  mtab._v_pathname,
                                                                  100 * mtab.size_on_disk / mtab.size_in_memory))
        relPathToTabNode = str(os.path.relpath(mFile.filename, self.dataroot_path) +
                               ":" + mtab._v_pathname)
        return g1, g2, relPathToTabNode

    def _get_maches_filehandle(self):
        if (self._last_match_file is None or
                    self._last_match_file.get_filesize() > MAX_MATCH_FILE_SIZE_SOFT):
            if not self._last_match_file is None:
                self._last_match_file.close()

            fname = os.path.join(self.matches_filepath, str(uuid.uuid4()) + ".h5")

            try:
                self._last_match_file = tb.open_file(fname, 'a', filters=self._compr)
                self.logger.info('open {} for appending'.format(self._last_match_file.filename))
            except Exception as e:
                self.logger.error('cannot open {}: {}'.format(fname, e))
                raise
        return self._last_match_file


def callDarwinExport(func):
    tmpfile = "/tmp/darwinMatchExporter_%d.dat" % (os.getpid())
    drwCodeFn = os.path.abspath(os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'ExportFunctions.drw'))
    try:
        with open(os.devnull, 'w') as DEVNULL:
            p = subprocess.Popen(['darwin', '-q', '-B'], stdin=subprocess.PIPE,
                                 stderr=subprocess.PIPE, stdout=DEVNULL)
            p.communicate(input="outfn := '%s': ReadProgram('%s'): %s; done;"
                                % (tmpfile, drwCodeFn, func));
            if p.returncode > 0:
                raise DarwinException(p.stderr.read())

        trans_tab = "".join(str(unichr(x)) for x in xrange(128)) + " " * 128
        with open(tmpfile, 'r') as jsonData:
            rawdata = jsonData.read()
            data = json.loads(rawdata.translate(trans_tab));
    finally:
        silentremove(tmpfile)
    return data


def queue_feeder(job_queue, tasks, nr_workers):
    """Process routine to put tasks in a job_queue.

    Once there are no more pairs, the process puts a None-sentinel
    for each of the workers into the queue to signal the end
    of work.

    For the moment being, tasks must be a list. A general iterable
    blocks for some unknown reason (TODO: fix it)"""
    totTasks = len(tasks)
    for i, task in enumerate(tasks):
        while True:
            try:
                job_queue.put(task, timeout=1.0)
                package_logger.info('queued %s (%d/%d; %.2f%% done)' % (
                    str(task), i, totTasks, 100.0 * i / totTasks))
                break
            except Queue.Full:
                wait = 1.0
                package_logger.info('job_queue full, retry in %f sec' % (wait))
                time.sleep(wait)
    for c in xrange(nr_workers):
        job_queue.put(None)


def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e:
        if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise  # re-raise exception if a different error occured


def getDebugLogger():
    import logging

    log = logging.getLogger('siblings')
    log.setLevel(logging.DEBUG)
    logHandler = logging.StreamHandler()
    logHandler.setLevel(logging.DEBUG)
    logHandler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    log.addHandler(logHandler)
    return log


def main(Lineage, path=""):
    log = getDebugLogger()
    x = DarwinFilesExporter(Lineage, path, logger=log)
    x.getAndStoreGenomeData()
    x.getAndStoreMatchData()
    x.close()


def verifyMatchesLinked(master, matchfile, link=True):
    matchpath = str(os.path.relpath(
        matchfile.filename,
        os.path.dirname(master.filename)))
    cnt_fixed = 0
    for node in matchfile.walk_nodes('/', classname='Table'):
        path = matchpath + ":" + node._v_pathname
        try:
            tax_pair = map(lambda z: 'tax%d' % (node.get_attr(z)), ('g1', 'g2'))
        except (AttributeError, TypeError):
            tax_pair_int = map(int, re.match(r'.*tax(\d+)[_/]tax(\d+)',
                                             node._v_pathname).groups())
            node.set_attr('g1', tax_pair_int[0])
            node.set_attr('g2', tax_pair_int[1])
            tax_pair = map(lambda z: 'tax%d' % (node.get_attr(z)), ('g1', 'g2'))

        for tax_pair_comb in itertools.permutations(tax_pair):
            expected_node = '/Matches/%s/%s' % (tax_pair_comb)
            if not expected_node in master:
                if link:
                    grp, tab = os.path.split(expected_node)
                    master.create_external_link(grp, tab, path)
                    cnt_fixed += 1
                else:
                    print('%s not linked as %s in %s' % (path, expected_node, master.filename))
            else:
                extlink = master.get_node(expected_node)
                if extlink.target != path:
                    print('%s does not link to %s' % (extlink.target, path))
    print('verified %s: fixed %d links\n' % (matchfile.filename, cnt_fixed))


if __name__ == "__main__":
    main("Halobacteria")
