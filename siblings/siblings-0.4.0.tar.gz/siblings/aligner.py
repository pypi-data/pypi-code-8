from __future__ import print_function, absolute_import, division
import hashlib
from builtins import dict
import pyopa
import math
import itertools
import time
import json
import zlib
import os
import bisect
import collections
import numpy
import tables
import base64
import platform
import logging

from .tablesformat import Matches as MatchesTab
from .zmq import MajorDomoWorker


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        """Extend default encode method if input object is a
        ndarray it will be converted into a dict holding dtype,
        shape and the data base64 encoded."""
        if isinstance(obj, numpy.ndarray):
            data_b64 = base64.b64encode(obj.data)
            return dict(__ndarray__=data_b64,
                        dtype=obj.dtype.descr,
                        shape=obj.shape)
        elif isinstance(obj, pyopa.AlignmentEnvironment):
            return None
        elif isinstance(obj, pyopa.Sequence):
            return str(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


def json_numpy_obj_hook(dct):
    """Decodes a previously encoded numpy ndarray
    with proper shape and dtype
    :param dct: (dict) json encoded ndarray
    :return: (ndarray) if input was an encoded ndarray
    """
    if isinstance(dct, dict) and '__ndarray__' in dct:
        data = base64.b64decode(dct['__ndarray__'])
        dtype = [(_[0].encode('ascii'), _[1].encode('ascii')) for _ in dct['dtype']]
        return numpy.frombuffer(data, dtype).reshape(dct['shape'])
    return dct


class Request(object):
    group1 = None
    group2 = None
    genome1 = None
    genome2 = None
    rID = None
    checksum = None

    def __init__(self, dct=None):
        if not dct:
            dct = {}
        for key in dct:
            if key in frozenset(['group1', 'group2', 'genome1', 'genome2', 'rID', 'checksum']):
                self.__setattr__(key, dct[key])

    @staticmethod
    def load_from_compressed_string(s):
        try:
            dct = json.loads(zlib.decompress(s), object_hook=json_numpy_obj_hook)
        except Exception:
            raise InvalidRequestFormat()
        req = Request(dct)
        if not req.validate_checksum():
            raise InvalidRequestFormat(req)
        return req

    def validate_checksum(self):
        return self.compute_checksum() == self.checksum

    def compute_checksum(self):
        md5 = hashlib.md5()
        for grp in ('group1', 'group2'):
            for prot in getattr(self, grp):
                md5.update(str(prot['entrynr']))
                md5.update(prot['seq'])
        md5.update(str(self.genome1))
        md5.update(str(self.genome2))
        md5.update(str(self.rID))
        return md5.hexdigest()

    def serialize_to_compressed_string(self):
        dct = {'genome1': self.genome1, 'genome2': self.genome2, 'rID': self.rID}
        for grp in ('group1', 'group2'):
            dct[grp] = [{'entrynr': _['entrynr'], 'seq': _['seq']} for _ in getattr(self, grp)]
        dct['checksum'] = self.compute_checksum()
        return zlib.compress(json.dumps(dct))


OPA = collections.namedtuple('OPA', ['score', 'pam', 'pamvar', 'env', 'start1', 'end1',
                                     'start2', 'end2', 'aligned_seq1', 'aligned_seq2', 'typ'])
Match = collections.namedtuple('Match', tables.dtype_from_descr(MatchesTab).names)


class Aligner(pyopa.MutipleAlEnv):
    """A class to compute optimal pairwise alignments and to quickly test for homology.

    This class provides methods to quickly test whether two amino adcid sequences are homologous
    given a certain alignment threshold. Further, the class provides a method to compute the
    local and global optimal pairwise alignment using SmithWaterman dynamic programming
    including distance optimisation, i.e. the scoring matrix is adjusted to the evolutionary
    distance and optimized for that."""

    def __init__(self, threshold):
        """creates an Aligner object

        :param threshold: the scoring threshold from when on an alignment is considered to be
         significant, i.e. two sequences are homologous."""
        log_pam1 = pyopa.read_env_json(os.path.join(pyopa.matrix_dir(), 'logPAM1.json'))
        #self.environments = pyopa.generate_all_env(log_pam1, 1266, threshold=threshold)
        self.environments = pyopa.load_default_environments()['environments']
        self.just_score_env = pyopa.generate_env(log_pam1, 224, threshold=threshold)
        super(Aligner, self).__init__(self.environments, log_pam1)
        self._pam_distances = [env.pam for env in self.environments]
        self._load_evalue_params()

    def _load_evalue_params(self):
        filename = os.path.join(os.path.dirname(__file__), 'data', 'altschul.gbc.fitted')
        self._evalue_params = numpy.genfromtxt(filename, names=True)

    def _find_nearest_env(self, pam_distance):
        """
        Searches for the environment with a PAM distance closest to 'pam_distance'

        :param pam_distance: the desired PAM distance
        :return: closest environment to pam_distance
        """
        index = bisect.bisect_right(self._pam_distances, pam_distance)

        if index == len(self._pam_distances):
            return self.environments[index - 1]
        return min(self.environments[index - 1], self.environments[index], key=lambda x: abs(x.pam - pam_distance))

    def fast_homology_test(self, seq1, seq2):
        """quickly test whether two sequences are homologous

        The test uses pyopa's implementation of the SmithWaterman algorithm that
        uses SSE instruction on a scoring matrix of shorts. See TODO:ref for details.

        :param seq1: the first sequence to be aligned
        :param seq2: the second sequence to be aligned
        :return bool: whether or not the sequences are homologous at the threshold level"""
        return pyopa.align_short(seq1, seq2, self.just_score_env) >= self.just_score_env.threshold

    def optimal_pairwise_alignment(self, seq1, seq2, modif='Local'):
        """computes the optimal pairwise alignment between two sequences

        This method computes the global or local optimal pairwise alignment
        between two sequences. The algorithm optimizes for the evolutionary
        distances that maximizes the alignment score. To obtain such an optimal
        alignment, several Smith-Watermann alignments are required and hence is
        a costly operation.

        :param seq1: the first sequence to be aligned
        :param seq2: the second sequence to be aligned.
        :param modif: (default Local) either ``Local`` or ``Global`` to specify which
          type of alignment should be computed.
        :return: an OPA instance"""
        max_score = -1e10
        tol = 1e-9
        do_global = modif.lower() == 'global'
        for pam in (35, 49, 71, 98, 115, 133, 152, 174, 200, 229, 262, 300):
            env = self._find_nearest_env(pam)
            #score_ref = pyopa.align_scalar_reference_local(seq1, seq2, env)
            score = pyopa.align_double(seq1, seq2, env, stop_at_threshold=False,
                                       is_global=do_global, calculate_ranges=True)
            aligned_seqs = pyopa.align_strings(seq1, seq2, env, is_global=do_global,
                                               provided_alignment=score)
            new_pam_est = self.estimate_pam(*aligned_seqs[0:2])
            if new_pam_est[0] > max_score:
                max_score = new_pam_est[0]
                opa = OPA(score=new_pam_est[0], pam=new_pam_est[1], pamvar=new_pam_est[2], env=env,
                          start1=score[3], end1=score[1], start2=score[4], end2=score[2],
                          aligned_seq1=aligned_seqs[0], aligned_seq2=aligned_seqs[1], typ=do_global)
        while True:
            env = self._find_nearest_env(opa.pam)
            if env == opa.env:
                break
            score = pyopa.align_double(seq1, seq2, env, stop_at_threshold=False,
                                       is_global=do_global, calculate_ranges=True)
            aligned_seqs = pyopa.align_strings(seq1, seq2, env, is_global=do_global,
                                               provided_alignment=score)
            new_pam_est = self.estimate_pam(*aligned_seqs[0:2])
            if new_pam_est[0] - score[0] < -tol * abs(new_pam_est[0]):
                logging.error('score decreased: {} - {} = {} < {}'
                              .format(new_pam_est[0], score[0], new_pam_est[0] - score[0],
                                      -tol*abs(new_pam_est[0])))
                with open('/tmp/error.dat', 'w') as fh:
                    fh.write(str(seq1))
                    fh.write('\n')
                    fh.write(str(seq2))
                    fh.write(modif.lower())
                raise ConvergenceError(opa)
            opa = OPA(score=score[0], pam=new_pam_est[1], pamvar=new_pam_est[2], env=env,
                      start1=score[3], end1=score[1], start2=score[4], end2=score[2],
                      aligned_seq1=aligned_seqs[0], aligned_seq2=aligned_seqs[1], typ=do_global)
        return opa

    def log_evalue(self, opa, len1=None, len2=None):
        """compute ln(evalue) for the given alignment"""
        row_idx = self._evalue_params['PAM'].searchsorted(opa.pam)
        if row_idx == len(self._evalue_params):
            row = self._evalue_params[row_idx - 1]
        else:
            row = min(self._evalue_params[row_idx - 1], self._evalue_params[row_idx],
                      key=lambda x: abs(x['PAM'] - opa.pam))

        if len1 is None:
            len1 = opa.end1 - opa.start1 + 1
        if len2 is None:
            len2 = opa.end2 - opa.start2 + 1
        len_corr = math.log(row['K'] * len1 * len2) / row['H']
        effLen1 = max(2, len1 - len_corr)
        effLen2 = max(2, len2 - len_corr)
        ln_e = -row['lambda'] * opa.score + math.log(row['K'] * effLen1 * effLen2)
        return ln_e

    def percent_identity(self, opa):
        """return percent identity of the given alignment"""
        ident = sum(itertools.imap(lambda x, y: x == y,
                                   opa.aligned_seq1.convert_readable(),
                                   opa.aligned_seq2.convert_readable()))
        return ident / len(opa.aligned_seq1)


class AlignWorker(MajorDomoWorker):
    """AlignWorker contains the server side code for computing alignments of siblings.

    This class communicates through a broker (MajorDomoBroker) with the Siblings
    database. The database initializes chunks of all-against-all comparisons which
    this worker computes (in parallel)."""

    def __init__(self, cfg):
        """initialize the Worker.
        :param cfg: a dict-like object containing configurations of the worker"""
        self.MIN_LENGTH = int(cfg.get('min_length', 30))
        self.MIN_OVERLAP_FRAC = float(cfg.get('min_overlap_frac', 0.3))
        self.MIN_SCORE = float(cfg.get('min_score', 130))
        self.FIXDBSIZE = int(cfg.get('size_searchdb', 20e6))
        self.user = cfg.get('user', 'anonymous')
        self.hostname = platform.node()
        try:
            self.hostname = self.hostname[0:self.hostname.index('.')]
        except ValueError:
            pass
        host = cfg.get('queue_host', 'siblings.ch')
        port = int(cfg.get('queue_port', 11295))
        self.url_queue = 'tcp://{host}:{port}'.format(host=host, port=port)
        self.aligner = Aligner(self.MIN_SCORE * 85 / 130)
        self.stop = False
        super(AlignWorker, self).__init__(self.url_queue, 'AllAll')

    def run_device(self):
        """main loop, started by the MajorDomoWorker."""
        response = None
        while not self.stop:
            try:
                qid, request = self.recv(response)
                response = [qid, self.handle_request(request)]
            except KeyboardInterrupt:
                self.stop = True
                logging.warn("interrupt received, stopping worker...")


    def handle_request(self, request):
        t_start = time.time()
        try:
            data = Request.load_from_compressed_string(request)
            result = self.compute_alignments(data)
        except AlignerException as e:
            result = e.to_reply()
        result['cputime'] = time.time() - t_start
        response = self.serialize(result)
        return response

    def _result_container(self, req):
        res = {'rID': req.rID, 'genome1': req.genome1, 'genome2': req.genome2,
               'user': self.user, 'host': self.hostname}
        return res

    def serialize(self, result):
        return zlib.compress(json.dumps(result, cls=NumpyEncoder))

    def compute_alignments(self, data):
        """compute the significant alignments of a job `Request`.

        :param data: a validated request object containing the sequences to be aligned
        :return dict: a reply ready dictionary containing a numpy array of type
          :class:`siblings.tablesformat.Matches` holding the significant matches data."""
        res = self._result_container(data)
        filt_function = lambda x: True
        if data.genome1 == data.genome2:
            filt_function = lambda tup: tup[0]['entrynr'] < tup[1]['entrynr']
        matches = []
        for p1, p2 in itertools.ifilter(filt_function, itertools.product(data.group1, data.group2)):
            for p in (p1, p2):
                if 'seq_obj' not in p:
                    p['seq_obj'] = pyopa.Sequence(p['seq'])
            try:
                if self.aligner.fast_homology_test(p1['seq_obj'], p2['seq_obj']):
                    opa = self.aligner.optimal_pairwise_alignment(p1['seq_obj'], p2['seq_obj'], modif='Local')
                    if (opa.score < self.MIN_SCORE or min(opa.end1 - opa.start1 + 1, opa.end2 - opa.start2 + 1) <
                        max(self.MIN_LENGTH, self.MIN_OVERLAP_FRAC * min(len(p1['seq']), len(p2['seq'])))):
                        continue
                    ln_e = self.aligner.log_evalue(opa, (len(p1['seq']) + len(p2['seq'])) / 2, self.FIXDBSIZE)
                    pident = self.aligner.percent_identity(opa)
                    glob_opa = self.aligner.optimal_pairwise_alignment(p1['seq_obj'], p2['seq_obj'], modif='Global')
                    glob_pident = self.aligner.percent_identity(glob_opa)
                    matches.append(Match(EntryNr1=p1['entrynr'], EntryNr2=p2['entrynr'], PamDistance=opa.pam,
                                         Score=opa.score, PamVariance=opa.pamvar, Start1=opa.start1, End1=opa.end1,
                                         Start2=opa.start2, End2=opa.end2, LogEValue=ln_e, PIdent=pident,
                                         Global_Score=glob_opa.score, Global_PamDistance=glob_opa.pam,
                                         Global_PamVariance=glob_opa.pamvar, Global_PIdent=glob_pident))
            except ConvergenceError as e:
                e.en1 = p1['entrynr']
                e.en2 = p2['entrynr']
                raise

        res['matches'] = numpy.array(matches, dtype=tables.dtype_from_descr(MatchesTab))
        return res


class AlignerException(Exception):
    def to_reply(self):
        res = {'code': 500, 'msg': self.message}
        for attr in vars(self):
            if not attr.startswith('_') and attr != 'message':
                res[attr] = getattr(self, attr)
        return res


class InvalidRequestFormat(AlignerException):
    def __init__(self, req=None):
        super(InvalidRequestFormat, self).__init__('Malformed request')
        try:
            self.rID = req.rID
        except AttributeError:
            pass


class ConvergenceError(AlignerException):
    def __init__(self, opa):
        super(ConvergenceError, self).__init__('Convergence error during alignment')
        self.opa = opa

