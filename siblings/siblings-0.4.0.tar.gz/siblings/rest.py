"""
The rest module provides a RESTful API using python tornado
framwork.
"""
from __future__ import print_function, absolute_import
import traceback
import json
import logging

import numpy as np
import tornado.web
import tornado.gen
import tornado.ioloop
from tornado.options import options, parse_config_file
from zmq.eventloop import ioloop

from .db import Reader, NotFound, KernelFilterNotSupported
from . import __version__

__author__ = 'adriaal'


def serializer_from_header(headers):
    try:
        content_type = headers['Accept']
    except KeyError:
        return JSONSerializer()

    for json_like in ("application/json", "text/javascript"):
        if content_type.find(json_like) >= 0:
            return JSONSerializer()
    if content_type.find("text/csv") >= 0:
        return CSVSerializer()
    elif content_type.find('text/html') >= 0:
        return HTMLSerializer()
    elif content_type.find('*/*') >= 0:
        return JSONSerializer()
    else:
        raise AcceptTypeError("Accept type not supported: {0:s}".format(content_type))


def numpy_to_dictlist(obj):
    fields = obj.dtype.names
    return [dict(zip(fields, val)) for val in obj]


class AcceptTypeError(Exception):
    pass


class NumpyAwareJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray) and obj.ndim == 1:
            if obj.dtype.names is None:
                return obj.tolist()
            else:
                return {"data": obj.tolist(), "columns": obj.dtype.names}
        elif isinstance(obj, np.generic):
            return obj.item()
        return json.JSONEncoder.default(self, obj)


class JSONSerializer(object):
    def encode(self, obj, **kwargs):
        return json.dumps(obj, cls=NumpyAwareJSONEncoder)

    def content_type(self):
        return "application/json; charset=UTF-8"


class CSVSerializer(object):
    def encode(self, obj, **kwargs):
        raise NotImplementedError()

    def content_type(self):
        return "text/csv; charset=UTF-8"

class HTMLSerializer(object):
    def encode(self, data, req_handler, template=None, **kwargs):
        if template is None:
            template = "data.html"
            data = json.dumps(data, cls=NumpyAwareJSONEncoder)
        return req_handler.render_string(template, data=data, **kwargs)

    def content_type(self):
        return "text/html; charset=UTF-8"


class RestHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(RestHandler, self).__init__(*args, **kwargs)
        self.log = self.application.log
        self.db = self.application.db
        self.serializer = serializer_from_header(self.request.headers)

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def set_default_headers(self):
        if not (__name__ is "__main__" or __version__ is None):
            self.set_header("Server", "{}/{} tornado/{}".format(
                __name__, __version__, tornado.version))
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers",
                        "Content-Type, Cookie, Authorization")
        self.set_header("Access-Control-Allow-Methods",
                        self.header_allowed_methods())
        self.set_header("Access-Control-Max-Age", 86400)

    def header_allowed_methods(self):
        return "GET,POST,OPTIONS"

    def respond(self, data=None, code=200, **kwargs):
        self.set_header("Content-Type", self.serializer.content_type())
        self.write(self.serializer.encode(data, req_handler=self, **kwargs))
        self.set_status(code)
        self.flush()
        self.finish()

    def write_error(self, status_code, **kwargs):
        """
        This method overwrites the default implementation by respecting the
        serializers return type.
        """
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            # in debug mode, try to send a traceback
            self.set_header('Content-Type', 'text/plain')
            for line in traceback.format_exception(*kwargs["exc_info"]):
                self.write(line)
            self.finish()
        else:
            self.set_header('Content-Type', self.serializer.content_type())
            self.write(self.serializer.encode({
                "code": status_code,
                "message": self._reason,
                }, req_header=self, template="error.html"))
            self.finish()

    def options(self, *args, **kwargs):
        self.respond()

    def get_body_arguments(self):
        return json.loads(self.request.body.decode("UTF-8"))

    def get_body_argument(self, name):
        return self.get_body_arguments()[name]


class ListGenomesHandler(RestHandler):

    #@tornado.web.authenticated
    def get(self):
        """List all the available genomes.

        This share point returns a list with summary information on the
        available genomes.

        **Example request**:

        .. sourcecode:: http

           GET /api/genomes HTTP/1.1
           Host: siblings.ch
           Accept: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json; charset=UTF-8

            [
              {
                "NCBITaxonId": 9606,
                "UniProtSpeciesCode": "HUMAN",
                "TotEntries": 31540,
                "SciName": "Homo sapiens",
                "DBRelease": "Ensembl 70; GRCh37; 12-DEC-2012""
              },
              {
                "NCBITaxonId": 9605,
                "UniProtSpeciesCode": "PANTR",
                "TotEntries": 30522,
                "SciName": "Pan trygolis",
                "DBRelease": "Ensembl 75"
              }
            ]
        """
        self.respond(numpy_to_dictlist(self.db.get_genomes()))


class MainHandler(RestHandler):
    def get(self):
        self.respond({}, template="home.html")

    def header_allowed_methods(self):
        return "GET,OPTIONS"


class MatchesHandler(RestHandler):

    def get(self, taxid1, taxid2):
        """Return homologous matches between a genome pair

        Summary information about the homologs between the genome
        pair is returned in form of a matrix, where each row
        corresponds to a relation between to proteins. The columns
        of the matrix hold the properties of the alignment, i.e.

        * the two homologous proteins (``EntryNr1`` and ``EntryNr2``)
        * the alignment ``Score`` computed using Smith-Waterman on
          a local alignment
        * an maximum likelihood estimation of the evolutionary
          distance ``PamDistance`` in PAM units
          (Percent accepted mutations). In addition, the
          ``PamVariance`` is an ML estimate of the variance for the
          ``PamDistance``.
        * the ranges of the two proteins that span the local alignment
          (``Start1``, ``End1``, ``Start2``, ``End2``). Positions
          are relative from the start of the protein sequences and
          are 1 based, e.g. if the alignment includes the first
          amino acid, the range will start at 1.
        * the ``LogEValue``, a transformed E-Value of the alignment
          using the ln() function to save precision.
        * the percent identity of the alignment in ``PIdent``.
        * ``Global_{Score, PamDistance, PamVariance, PIdent}`` store
          the same properties based on the global alignment.

        :param taxid1: Taxonomy Id of first genome
        :param taxid2: Taxonomy Id of second genome
        :>json colnames: column names / properties of the alignments.
        :>json data: the data matrix. Each row corresponds to one significant alignment.
        :status 200: success
        :status 400: the query cannot be parsed.
        :status 404: at least one genome wasn't found in the dataset.

        **Example request**:

        .. sourcecode:: http

           GET /api/matches/9606/9606 HTTP/1.1
           Host: siblings.ch
           Accept: application/json
        """
        try:
            taxid1, taxid2 = int(taxid1), int(taxid2)
            res = self.db.get_matches_between_genomes(taxid1, taxid2)
            self.respond(res)
        except NotFound as e:
            raise tornado.web.HTTPError(404)

    def post(self, taxid1, taxid2):
        """Return homologous matches between a genome pair with filtering options.

        Same as :py:method:`get`, but allows for additional filtering options by
        passing a filter string attribute. Several conditions can be combined with
        the "&" operator (logical and) and can operate on all the attributes of the
        returned matches table.

        :param taxid1: Taxonomy Id of first genome
        :param taxid2: Taxonomy Id of second genome
        :>json colnames: column names / properties of the alignments.
        :>json data: the data matrix. Each row corresponds to one significant alignment.
        :status 200: success
        :status 400: the query or filters cannot be parsed.
        :status 404: at least one genome wasn't found in the dataset.

        **Example request**:
        return matches that have a score >2000 and an evolutionary distance of less
        than 15 PAM:

        .. sourcecode:: http

           GET /api/matches/9606/10090 HTTP/1.1
           Host: siblings.ch
           Accept: application/json
           Content-type: application/json
           [BODY data: {"filter": "Score>2000 & PamDistance<15"}]
        """

        try:
            body_args = self.get_body_arguments()
            filter_obj = None
            taxid1, taxid2 = int(taxid1), int(taxid2)
            filter_str = body_args.get('filter', '')
            if filter_str != "":
                filter_obj = self.db.query_filter(filter_str)
        except KernelFilterNotSupported:
            raise tornado.web.HTTPError(400)
        except (KeyError, ValueError) as e:
            logging.exception('unexpeced expetion')
            raise tornado.web.HTTPError(400)

        try:
            res = self.db.get_matches_between_genomes(taxid1, taxid2, filter_obj)
            self.respond(res)
        except NotFound as e:
            raise tornado.web.HTTPError(404)


class GenomeDetailHandler(RestHandler):
    def get(self, taxid):
        """Get the protein sequences of a query genome.

        The method returns a list with the protein sequence and
        -- if selected with the boolean flag cdna -- the coding DNA
        sequence for a set of selected entries.

        :param int taxid: the NCBI taxonomy id of the query genome.
        :return: a list of dicts ``EntryNr``, ``Sequence`` and
         ``cDNA`` elements for the requested entry numbers.
        :status 200: success
        :status 404: the genome wasn't found in the dataset.
        **Example request**:

        .. sourcecode:: http

           GET /api/genome/9606 HTTP/1.1
           Host: siblings.ch
           Accept: application/json
        """
        taxid = int(taxid)
        try:
            res = self.db.get_genome_sequences(taxid, cDNA=True)
            self.respond(res)
        except NotFound as e:
            raise tornado.web.HTTPError(404)

    def post(self, taxid):
        """Upload a new genome to be included.

        Using this method, users can contribute new genomes to be
        included into the dataset. They are automatically added
        to the queue for all-against-all compuations and eventually
        will become available in this service for download again.
        Obviously, the computation will require a significant amount
        of time and hence this will take usually several days or weeks,
        depending on the number of pending genomes, their sizes and the
        number of available compute nodes.

        The uploaded genome needs to be a json encoded string containing
        the following attributes:

        :param int taxid: the NCBI taxonomy id of the new genome.
        :<json str SciName: the scientific name of the genome (including strain information)
        :<json [str] Sequences: the amino acid sequences of the genomes. These sequences are
          used to compute the all-against-all.
        :<json [str] cDNA: the corresponding cDNA sequences.
        """
        try:
            body_args = self.get_body_arguments()
            taxid = int(taxid)
        except ValueError:
            raise tornado.web.HTTPError(400)

        raise NotImplementedError('This function is not yet available')
        genome = body_args['genome']
        email = body_args['email']



class TimingsHandler(RestHandler):
    def get(self):
        """Get summary timing statistics of all users contributing
        computations.

        The method returns a dictionary with the contributed number of
        All-against-all units, their average duration and the total
        contributed cpu time in seconds per user (and host).

        If a html page is requested (using the Accept header), this
        information is rendered as a html page including graphics, otherwise
        a json encoded object is returned.

        :status 200: success
        """
        timings = self.db.get_timings_stats()
        self.respond(timings, template="rest_timings.html")

    def header_allowed_methods(self):
        return "GET, OPTIONS"


class Application(tornado.web.Application):
    def __init__(self, database, test=False, *args, **kwargs):
        handlers = [
           (r"/", MainHandler),
           (r"/api/genomes/?", ListGenomesHandler),
           (r"/api/genomes/(?P<taxid>\d+)", GenomeDetailHandler),
           (r"/api/matches/(?P<taxid1>\d+)/(?P<taxid2>\d+)/?", MatchesHandler),
           (r"/(?:api/)?timings/?", TimingsHandler),
        ]
        super(Application, self).__init__(handlers, **kwargs)
        self.log = logging.getLogger(__name__)
        self.log.addHandler(logging.FileHandler("mainlog.log", mode="w"))
        self.db = database


def start():
    from .settings import settings
    app = Application(Reader(options.db), **settings)
    ioloop.install()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    start()