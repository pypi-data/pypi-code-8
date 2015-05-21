from __future__ import print_function, division, absolute_import
from builtins import super, range
import os
import collections
import numpy
import tables
import uuid
import math
import time
import logging
import zlib
import json
import zmq
from hashlib import md5

from .tablesformat import Matches as MatchesTableFmt
from .tablesformat import Timings, JobsToExecute, PairStatus, Genome, XRef, Protein
from .zmq import MajorDomoClient
from .aligner import Request, json_numpy_obj_hook


class AllAllJobScheduler(MajorDomoClient):
    """Scheduler of pending AllAll jobs

    This class is responsible to schedule allall-jobs for new genomes, sending
    the relevant jobs to the workers and storing the results in the hdf5 database.
    """

    def __init__(self, writer=None, cfg=None, verbose=False):
        if cfg is None: cfg = {}
        host = cfg.get('queue_host', 'siblings.ch')
        port = int(cfg.get('queue_port', 11295))
        self.MAX_OPEN_REQ = int(cfg.get('max_open_req', 1000))
        self.url_queue = 'tcp://{host}:{port}'.format(host=host, port=port)
        super(AllAllJobScheduler, self).__init__(self.url_queue, verbose=verbose)
        if writer is None:
            writer = Writer(cfg['database'], cfg)

        self.setsockopt(zmq.IDENTITY, md5(writer.db_path.encode('utf-8')).hexdigest()[0:8])
        self.writer = writer
        self._count_of_open_requests = 0

    def run_device(self):
        last_job_report_at = 0
        while True:
            try:
                reply = self.recv()
                if not reply is None:
                    self._count_of_open_requests -= 1
                    rID, reply = reply
                    reply = json.loads(zlib.decompress(reply), object_hook=json_numpy_obj_hook)
                    self.writer.store_reply(reply)
                # TODO: make this more dynamic and robust.
                if self._count_of_open_requests < self.MAX_OPEN_REQ:
                    req = self.writer._next_request()
                    self.send('AllAll', [req.rID, req.serialize_to_compressed_string()])
                    self._count_of_open_requests += 1
            except QueueEmptyError:
                for k, (g1, g2) in enumerate(self.writer.find_missing_alignments()):
                    if k > 5:
                        break
                    self.writer.add_genomepair_to_jobqueue(g1, g2)
            except ImportDataError as e:
                logging.exception(u"Q: erroneous reply for {}:\n --> '{}'".format(rID, reply))
                self.writer.mark_job_as_error(rID)
            except KeyboardInterrupt:
                logging.info('Q: leaving main loop')
                break
            finally:
                if self.verbose:
                    logging.info('Q: {0:d} open requests.'.format(self._count_of_open_requests))
                if time.time() - last_job_report_at > 300:
                    stats = self.writer.count_jobs_enqueued_and_ready()
                    logging.info('job status: {!r}'.format(stats))
                    logging.info('Q: {0:d} open requests.'.format(self._count_of_open_requests))
                    last_job_report_at = time.time()
        self.writer.close()


class LRUCache(object):
    def __init__(self, capacity, cache_leave_callable=None):
        self.capacity = capacity
        self.cache = collections.OrderedDict()
        self.cache_leave_callable = cache_leave_callable

    def get(self, key):
        try:
            value = self.cache.pop(key)
            self.cache[key] = value
            return value
        except KeyError:
            return -1

    def set(self, key, value):
        try:
            self.cache.pop(key)
        except KeyError:
            if len(self.cache) >= self.capacity:
                (remKey, remVal) = self.cache.popitem(last=False)
                if not self.cache_leave_callable is None:
                    self.cache_leave_callable(remKey, remVal)
        self.cache[key] = value


class Writer(object):
    def __init__(self, db_path, cfg):
        self.MAX_FILE_SIZE_SOFT = dict(genomes=int(cfg.get('max_filesize_genomes', 5e8)),
                                       matches=int(cfg.get('max_filesize_allall', 2e9)))
        self.JOBSIZE = int(cfg.get('jobsize', 1e11))
        self.TIMEOUT = int(cfg.get('max_time_job_done', 3600 * 10))
        self.MAX_RETRY_ON_ERROR = int(cfg.get('max_retry_on_error', 2))
        self.db_path = os.path.abspath(os.path.normpath(
            os.path.expanduser(db_path)))
        self.db_handle = None
        self.nodes_lookup = {'queuetab': ('/jobs/queue', JobsToExecute),
                             'timingtab': ('/stats/timings', Timings),
                             'pairstattab': ('/stats/computations', PairStatus),
                             'summarytab': ('/Genomes/Summaries', Genome),
                             'xreftab': ('/Genomes/XRefs', XRef)}
        self._last_file = {}
        self.compress = tables.Filters(5, 'zlib', shuffle=True, fletcher32=True)
        self.logger = logging.getLogger(__name__)
        self.init_db()

    def close(self):
        if not self.db_handle is None:
            self.db_handle.close()
        for fh in self._last_file.values():
            fh.close()

    def init_db(self):
        self.close()
        self.db_handle = tables.open_file(self.db_path, mode='a', filters=self.compress)
        self._ensure_tables()

    def _ensure_tables(self):
        for path, desc in self.nodes_lookup.values():
            grp, sep, name = path.rpartition('/')
            try:
                self.db_handle.create_table(grp, name, desc, createparents=True)
            except tables.NodeError:
                pass

    def _get_node(self, name, follow_link=True):
        if name.startswith('/'):
            node = self.db_handle.get_node(name)
        else:
            node = self.db_handle.get_node(self.nodes_lookup[name][0])
        if follow_link and isinstance(node, tables.link.Link):
            # open in same mode as master file
            node = node(mode=self.db_handle.mode)
        return node


    def add_genomepair_to_jobqueue(self, g1, g2):
        queuetab = self._get_node('queuetab')
        pairstattab = self._get_node('pairstattab')
        gstab = self._get_node('summarytab')
        gs = gstab.read_where('(NCBITaxonId == {0:d}) | (NCBITaxonId == {1:d})'.format(g1, g2))
        if len(gs) != len(set([g1, g2])):
            raise DBConsistencyError(u"Summary table contains unexpected "
                                     u"rows for {} and {}: {}".format(g1, g2, str(gs)))
        if g1 != g2:
            gs1, gs2 = gs[0], gs[1]
            if gs1['NCBITaxonId'] != g1:
                gs1, gs2 = gs2, gs1
        else:
            gs1 = gs2 = gs[0]
        prot_tabs = list(self._get_node('/Genomes/tax{0:d}'.format(g)) for g in (g1, g2))
        seq_lens = list(z.Entries.cols.SequenceBufferLength for z in prot_tabs)
        nr_prot_g1 = int(math.sqrt(self.JOBSIZE /
                                   (tables.Expr('sum(c)', {'c': seq_lens[1]}).eval()[0] /
                                    len(seq_lens[1]))))
        for x1 in range(0, gs1['TotEntries'], nr_prot_g1):
            nr_aa_in_g1_junk = sum(seq_lens[0][x1:x1 + nr_prot_g1])
            y2start = 0
            while y2start < gs2['TotEntries']:
                cells = 0
                for y2 in range(y2start, gs2['TotEntries']):
                    cells += nr_aa_in_g1_junk * seq_lens[1][y2]
                    if cells > self.JOBSIZE:
                        break
                row = queuetab.row
                row['JobId'] = uuid.uuid4().get_hex().encode('ascii')
                row['Genome1'] = g1
                row['Genome2'] = g2
                row['Range1'] = (x1, min(x1 + nr_prot_g1, gs1['TotEntries'] - 1))
                row['Range2'] = (y2start, max(y2start + 1, y2))
                row.append()
                y2start = y2 + 1
        queuetab.flush()
        for row in pairstattab.where('(Genome1 == {0:d}) & (Genome2 == {1:d})'.format(g1, g2)):
            row['Status'] = pairstattab.get_enum('Status').QUEUED
            row.update()
        pairstattab.flush()

    def find_missing_alignments(self):
        pairstattab = self._get_node('pairstattab')
        stat_enum = pairstattab.get_enum('Status')
        for row in pairstattab.where('Status=={0:d}'.format(stat_enum.NEW)):
            yield (row['Genome1'], row['Genome2'])

    def count_jobs_enqueued_and_ready(self):
        queuetab = self._get_node('queuetab')
        cnts = collections.defaultdict(int)
        curtime = time.time()
        for row in queuetab:
            if row['Submit_time'] < 0.1:
                cnts['ready'] += 1
            elif row['ErrorCount'] > self.MAX_RETRY_ON_ERROR:
                cnts['failed'] += 1
            elif row['Submit_time'] - curtime < self.TIMEOUT:
                cnts['running'] += 1
            else:
                cnts['redo'] += 1
        return cnts

    def _next_request(self):
        queuetab = self._get_node('queuetab')
        job_iter = queuetab.where('({0:f} - Submit_time > {1:f}) & (ErrorCount <= {2:d})'
                                  .format(time.time(), self.TIMEOUT, self.MAX_RETRY_ON_ERROR))
        try:
            job = job_iter.next()
        except StopIteration:
            raise QueueEmptyError()

        req = {'rID': job['JobId']}
        for g_nr in range(1, 3):
            g_str = 'Genome{0:d}'.format(g_nr)
            req[g_str.lower()] = job[g_str]
            grp = self._get_node('/Genomes/tax{0:d}'.format(job[g_str]))
            prottab = grp._f_get_child('Entries')
            seqbuf = grp._f_get_child('SequenceBuffer')
            ran_str = 'Range{0:d}'.format(g_nr)
            group = []
            for prot in prottab.iterrows(*job[ran_str]):
                group.append(dict(entrynr=prot['EntryNr'],
                                  seq=seqbuf[prot['SequenceBufferOffset']:
                                  prot['SequenceBufferOffset'] + prot['SequenceBufferLength']].
                                  tostring()))
            req['group{0:d}'.format(g_nr)] = group
        req_obj = Request(req)
        job['Submit_time'] = time.time()
        job.update()
        # consume rest of job_iter to be able to flush properly
        collections.deque(job_iter, maxlen=0)
        queuetab.flush()
        return req_obj

    def add_genome(self, data):
        gstab = self._get_node('summarytab')
        try:
            nr_entries = self._create_genomedb(data)
            #self._add_xrefs(data['NCBITaxonId'], data['xrefs'])
        except ImportDataError:
            logging.info('genome {} already in DB. Ignoring'.format(data['NCBITaxonId']))
            raise
        except DBConsistencyError:
            logging.error('could not add {} ({}):'.format(data['NCBITaxonId'], data['UniProtSpeciesCode']))
            raise
        else:
            gs = gstab.row
            gs['NCBITaxonId'] = data['NCBITaxonId']
            gs['UniProtSpeciesCode'] = data['UniProtSpeciesCode']
            gs['SciName'] = data['SciName']
            gs['DBRelease'] = data['Release']
            gs['TotEntries'] = nr_entries
            gs.append()
            gstab.flush()
            self._add_genome_pairs(data['NCBITaxonId'])

    def _rel_path_to_master_file(self, path):
        """returns the relative path with respect to the master hdf5 file"""
        return os.path.relpath(path, os.path.dirname(self.db_path))

    def _create_genomedb(self, data):
        g = data['NCBITaxonId']
        try:
            self.db_handle.get_node('/Genomes/tax{0:d}'.format(g))
            raise ImportDataError('genome {} already imported'.format(g))
        except tables.NoSuchNodeError:
            pass
        genome_file = self._get_filehandle('genomes')
        grp = '/tax{NCBITaxonId:d}/rel_{Release:s}/Proteins'.format(**data)
        entry_tab = genome_file.create_table(grp, "Entries", Protein,
                                             expectedrows=len(data['Entries']), createparents=True)
        seq_arr = genome_file.create_earray(grp, "SequenceBuffer", tables.StringAtom(1), (0,),
                                            "concatenated protein sequences",
                                            expectedrows=1000 * len(data['Entries']))
        dna_arr = genome_file.create_earray(grp, "DNABuffer", tables.StringAtom(1), (0,),
                                            "concatenated cDNA sequences",
                                            expectedrows=3000 * len(data['Entries']))
        for i, entry in enumerate(data['Entries']):
            eNr = i + 1
            entry_tab_row = entry_tab.row
            # write protein info in table
            entry_tab_row['EntryNr'] = eNr
            entry_tab_row['SequenceBufferOffset'] = seq_arr.nrows
            entry_tab_row['SequenceBufferLength'] = len(entry['Sequence'])
            entry_tab_row['DNABufferOffset'] = dna_arr.nrows
            entry_tab_row['DNABufferLength'] = len(entry['cDNA'])
            entry_tab_row['CanonicalId'] = entry.get('Id', '').encode('utf-8')
            entry_tab_row.append()
            # add sequences to buffers
            seq_arr.append(numpy.ndarray((len(entry['Sequence']),),
                                         buffer=entry['Sequence'].encode('ascii'),
                                         dtype=tables.StringAtom(1)))
            dna_arr.append(numpy.ndarray((len(entry['cDNA']),),
                                         buffer=entry['cDNA'].encode('ascii'),
                                         dtype=tables.StringAtom(1)))
        entry_tab.flush()
        seq_arr.flush()
        dna_arr.flush()
        rel_path_2_grp_node = str(self._rel_path_to_master_file(genome_file.filename) + ":" + grp)
        self.db_handle.create_external_link("/Genomes", "tax{0:d}".format(g), rel_path_2_grp_node)
        return len(entry_tab)

    def _add_xrefs(self, genome, xrefs):
        """add xrefs to proteins to the global xref table.

        xrefs is expected to be a list of tuples with
        [id/eNr, xref_source, xref]
        """
        xreftab = self._get_node('xreftab')
        sources = xreftab.get_enum('XRefSource')
        for ref in xrefs:
            # TODO: implement xref adding
            pass

    def _get_filehandle(self, typ='genomes'):
        if (self._last_file.get(typ, None) is None or
                    self._last_file[typ].get_filesize() > self.MAX_FILE_SIZE_SOFT[typ]):
            if not self._last_file.get(typ, None) is None:
                self._last_file[typ].close()

            folder = self._get_external_filepath(typ)
            if not os.path.isdir(folder):
                os.makedirs(folder)
            fname = os.path.join(folder, str(uuid.uuid4()) + ".h5")

            try:
                self._last_file[typ] = tables.open_file(fname, 'a', filters=self.compress)
                self.logger.info('open {} for appending'.format(self._last_file[typ].filename))
            except Exception as e:
                self.logger.error('cannot open {}: {}'.format(fname, e))
                raise
        return self._last_file[typ]

    def _get_external_filepath(self, typ):
        folder, name = os.path.split(self.db_path)
        return os.path.join(folder, typ)

    def _add_genome_pairs(self, cur_genome):
        gs = self._get_node('summarytab')
        pairtab = self._get_node('pairstattab')
        stat_new = pairtab.get_enum('Status').NEW
        for genome in gs:
            row = pairtab.row
            row['Genome1'] = cur_genome
            row['Genome2'] = genome['NCBITaxonId']
            row['Status'] = stat_new
            row.append()
        pairtab.flush()
        self.logger.info(u"added {0:d} genome pairs to pending pairs".format(len(gs)))

    def _update_pairstats(self, g1, g2):
        # this was last job in this genome pair. change status in PairStatus
        pairstattab = self._get_node('pairstattab')
        stat_enum = pairstattab.get_enum('Status')
        found = 0
        for pair in pairstattab.where('(Genome1 == {0:d}) & (Genome2 =={1:d})'
                                           .format(g1, g2)):
            pair['Status'] = stat_enum.COMPUTED
            pair.update()
            found += 1
        pairstattab.flush()


    def store_reply(self, reply):
        """store reply of align workers in pytable.

        Replies from alignment workers are processed in this
        method. The JobQueue and PairStatus tables are updated
        accordingly. Replies which do not conform to the
        expected format are ignored and a :class:`ImportDataError`
        is raised.

        The method also updates the computation providing user
        statistics."""
        try:
            jobId = reply['rID']
        except KeyError:
            self.logger.warn(u"received invalid reply. skipping reply.")
            raise ImportDataError()

        queuetab = self._get_node('queuetab')
        jobs = queuetab.get_where_list('JobId == b"{}"'.format(jobId))
        if len(jobs) < 1:
            self.logger.info(u"received reply of job that hasn't been queued: {}".format(jobId))
            raise ImportDataError()
        elif len(jobs) > 1:
            self.logger.error(u"job with id '{}' multiple times in queue table.".format(jobId))
            raise DBConsistencyError(u"job with id '{}' multiple times in queue table.".format(jobId))
        job = queuetab[jobs[0]]
        if not self._check_data_ranges(reply, job):
            raise ImportDataError()
        self._write_matches(reply)
        self._update_timingstats(reply)
        g1, g2 = job['Genome1'], job['Genome2']
        try:
            queuetab.remove_row(jobs[0])
            queuetab.flush()
        except NotImplementedError as e:
            # this can happen if only one element is in table. apparently
            # hdf5 does not allow to remove such rows. The fix is to remove
            # the table and recreate it.
            queuetab.remove()
            self._ensure_tables()
            queuetab = self._get_node('queuetab')

        if len(queuetab.get_where_list('(Genome1 == {0:d}) & (Genome2 == {1:d})'
                .format(g1, g2))) == 0:
            self._update_pairstats(g1, g2)

    def _check_data_ranges(self, reply, job):
        """minimal sanity check on reply data

        this method checks for obvious inconsistencies in the
        replied matches table. It checks whether the entry nrs
        are compatible with the original :py:meth:`Request`."""
        matches = reply['matches']
        if len(matches) > 0:
            entryNrs = matches[['EntryNr1', 'EntryNr2']].view(dtype='u4').reshape(len(matches), 2)
            mins = entryNrs.min(axis=0)
            maxs = entryNrs.max(axis=0)
            if (mins[0] <= job['Range1'][0] or mins[1] <= job['Range2'][0] or
                        maxs[0] > job['Range1'][1]+1 or maxs[1] > job['Range2'][1]+1):
                self.logger.info('ranges do not match: mins: {}, maxs: {}, Range1: {}, Range2: {}'
                                 .format(mins, maxs, job['Range1'], job['Range2']))
                return False
        return True

    def _write_matches(self, reply):
        """write matches of reply into pytable db"""
        match_path = '/Matches/tax{genome1:d}/tax{genome2:d}'.format(**reply)
        try:
            tab = self._get_node(match_path)
        except tables.NoSuchNodeError:
            fh = self._get_filehandle('matches')
            tabdir, tabname = '/tax{0:d}'.format(reply['genome1']), 'tax{0:d}'.format(reply['genome2'])
            tab = fh.create_table(tabdir, tabname, MatchesTableFmt, expectedrows=2e6, createparents=True)
            tab.set_attr('g1', reply['genome1'])
            tab.set_attr('g2', reply['genome2'])
            rel_path_2_matches = str(self._rel_path_to_master_file(fh.filename) + ":" + tab._v_pathname)
            node, name = match_path.rsplit('/', 1)
            self.db_handle.create_external_link(node, name, rel_path_2_matches, createparents=True)
        if tab.get_attr('g1') != reply['genome1'] or tab.get_attr('g2') != reply['genome2']:
            raise DBConsistencyError('unexpected genome order: {}/{}'
                                     .format(reply['genome1'], reply['genome2']))
        tab.append(reply['matches'])

    def mark_job_as_error(self, jobId):
        """increase error count on job.

        If the error count becomes too high, job won't be send anymore
        to be computed."""
        try:
            queuetab = self._get_node('queuetab')
            for row in queuetab.where('JobId == b"{}"'.format(jobId)):
                row['ErrorCount'] += 1
                row.update()
            queuetab.flush()
        except Exception:
            self.logger.exception('exception while marking job as error')


    def _update_timingstats(self, reply):
        timetab = self._get_node('timingtab')
        cnts = 0
        try:
            # make sure the user and host argument are not longer than the respective fields
            query_param = dict([(field, reply[field][0:timetab.coldtypes[field.capitalize()].itemsize])
                                for field in ('host', 'user')])
            for row in timetab.where('(User == b"{user:s}") & (Host == b"{host:s}")'.format(**query_param)):
                row['Total_nr_jobs'] += 1
                row['Total_time'] += reply['cputime']
                row['Total_time2'] += reply['cputime']**2
                row.update()
                cnts += 1
            if cnts == 0:
                row = timetab.row
                row['User'] = query_param['user']
                row['Host'] = query_param['host']
                row['Total_nr_jobs'] = 1
                row['Total_time'] = reply['cputime']
                row['Total_time2'] = reply['cputime']**2
                row.append()
            timetab.flush()
        except KeyError as e:
            self.logger.info('incomplete timing statistics found: {}'.format(e))


class ImportDataError(Exception):
    pass


class DBConsistencyError(Exception):
    pass


class QueueEmptyError(Exception):
    pass