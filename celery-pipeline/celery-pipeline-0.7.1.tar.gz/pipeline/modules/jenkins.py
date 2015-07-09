""" Jenkins API

TODO:
    Mayneed to support multiple sources.
    We are using inheritance,we may need to switch to composition

THIS DOES NOT WORK.  OLD CODE.
This module is not registered in pipeline.__init__.
"""
from urllib.request import urlopen, Request, build_opener, ProxyHandler, install_opener
import urllib
import json
from urllib.error import HTTPError
import base64
from jenkinsapi.api import get_artifacts
from jenkinsapi.jenkins import Jenkins
try:
    from urllib.parse import urlparse
except ImportError:
    import urlparse

from pipeline.actions import action, TaskResult
from pipeline.bases import Source
from pipeline.modules.github.pullrequest import PullRequest
from pipeline.tasks import TaskResult
import logging
logger = logging.getLogger(__name__)
from pipeline.command import CommandResult

class ArtifactTaskResult(TaskResult):
    # this is getting a little ridiculous.
    #need to replace 'Source' with a writable Context
    def __init__(self, result, artifact_url, user, passwd):
        super(ArtifactTaskResult, self).__init__(result)
        self.url = artifact_url
        self.user = user
        self.passwd = passwd


@action(name='jenkins-artifact')
def jenkins_artifact(self, retval, source, **kwargs):
    """Pull an artifact from jenkins.
    """
    def auth_headers(username, password):
        s = '{}:{}'.format(username, password)
        b = bytes(s, 'ascii')
        return 'Basic {}'.format(
            base64.b64encode(b).decode('ascii')
        )

    artifact_file = kwargs.pop('artifact')

    parsed = urlparse(source.target_url)
    jenkins = "{}://{}".format(
        parsed.scheme, parsed.netloc
    )
    parts = parsed.path.split('/')

    job = parts[2]
    build = parts[3]

    prxy = ProxyHandler({})
    opener = build_opener(prxy)
    install_opener(opener)
    #TODO move to env var
    auth = auth_headers('E001882', '567aca75e52ccdf8f4feaf5f367c7c04')
    api_url = '{}/job/{}/{}/api/json'.format(jenkins, job, build)
    req = Request(api_url)
    req.add_header('Authorization', auth)
    try:
        response =  urlopen(req).read()
    except HTTPError as ex:
        logger.critical(ex)
        return TaskResult(False)

    data = json.loads(response.decode('utf-8'))
    artifacts = data['artifacts']
    for artifact in artifacts:
        if artifact['fileName'] == artifact_file:
            artifact_url = '{}/job/{}/{}/artifact/{}'.format(jenkins, job, build, artifact['relativePath'])
            #req = Request(artifact_url)
            #req.add_header('Authorization', auth)
            #try:
            #    response =  urlopen(req).read()
            #except HTTPError as ex:
            #    logger.critical(ex)
            #    return TaskResult(False)
            
            return ArtifactTaskResult(True, artifact_url, 'E001882', '567aca75e52ccdf8f4feaf5f367c7c04')

    logger.error('Didnt find artifact {} at {}'.format(artifact_file, api_url))
    return TaskResult(False)


class PrBuilderStatusSource(PullRequest):
    __id = 'pr_status'
    
    def __init__(self, build_url, *args, **kwargs):
        self.target_url = build_url
        super(PrBuilderStatusSource, self).__init__(*args, **kwargs)

#import time
#import urllib
#import uuid
#import simplejson as json
#from simplejson.decoder import JSONDecodeError
#import logging
##from enum import Enum
#import requests
#from requests.exceptions import HTTPError
#from datetime import timedelta
#
#from django.conf import settings
#
#
##logging.basicConfig()
#log = logging.getLogger(__name__)
#
#class BuildError(Exception):
#    pass
#
#class Jenkins(object):
#    def __init__(self, host, user, token):
#        self.host = host
#        self.user = user
#        self.token = token
#
#class ParameterizedJob(object):
#    """
#    deals with https://issues.jenkins-ci.org/browse/JENKINS-13546
#        - requires the job contain an 'ident' param do we can
#        figure out it's build number from the queue.
#    """
#    def __init__(self, jenkins, job_name):
#        self.jenkins = jenkins
#        self.job_name = job_name
#        self.ident = uuid.uuid4()  # needed to find the jobid
#        self.queue__id = None
#        self.build_number = None
#        self.session = requests.Session()
#
#    def build(self, **job_params):
#
#        params = job_params.copy()
#        params.update({
#            'token': self.jenkins.token,
#            'delay': settings.BUILD_SUBMIT_DELAY,
#            'ident': self.ident
#        })
#        url = "{0}/job/{1}/buildWithParameters?{2}".format(
#            self.jenkins.host, self.job_name, urllib.urlencode(params)
#        )
#        log.debug("building jenkins job at %s" % url)
#
#        try:
#            # enqueue the job
#            resp = self.session.get(url, auth=(self.jenkins.user, self.jenkins.token))
#            resp.raise_for_status()
#        except HTTPError as e:
#            log.error("error queueing jenkins job %s" % str(e))
#        else:
#            # find our job in the queue
#            self.queue__id = self.get_queue__id()
#            if self.queue__id is None:
#                raise BuildError("Couldn't get queue id")
#
#            # get our build number
#            self.build_number = self.poll_for_build_number()
#            if self.build_number is None:
#                raise BuildError("Couldn't find job number")
#
#    def get_queue_id(self):
#        """Find a job the job queue, using an artificial `ident` parameter that
#        was passed into the build.
#        This is required until Jenkins bug https://issues.jenkins-ci.org/browse/JENKINS-13546
#        is resolved.
#        """
#        log.debug('attempting to get queue id for our job %s' % self.job_name)
#        try:
#            resp = self.session.get("%s/queue/api/json" % self.jenkins.host)
#            resp.raise_for_status()
#            queue = json.loads(resp.content)
#        except HTTPError as e:
#            log.error("http error getting queue id %s" % str(e))
#        except JSONDecodeError:
#            log.error("erorr decoding response")
#        else:
#            for item in queue['items']:
#                if not item['task']['name'] == self.job_name:
#                    continue
#                params = [a['parameters'] for a in item['actions'] if 'parameters' in a][0]
#                ident_param = [i['value'] for i in params if i['name'] == 'ident'][0]
#                if ident_param == unicode(self.ident):
#                    log.debug("found queue id for job")
#                    return str(item['id'])
#
#    def poll_for_build_number(self):
#        """Find a job's build id in the queue details.
#        The build ID is not immediately available when the job is queued.
#
#        Make a queue api request each ``QUEUE_POLL_WAIT`` seconds until a response
#        containing build number is received, or ``QUEUE_POLL_MAX_WAIT`` seconds is reached.
#        """
#        max_wait = settings.QUEUE_POLL_MAX_WAIT
#        while True:
#            try:
#                log.debug('attempting to get build number for queue item %s' % self.queue_id)
#                response = self.session.get(
#                    "%s/queue/item/%s/api/json" % (self.jenkins.host, self.queue_id)
#                )
#                response.raise_for_status()
#                queue_info = json.loads(response.content)
#            except HTTPError as e:
#                log.warning("could not get the jenkins build number %s; bailing" % str(e))
#                break
#            except JSONDecodeError:
#                log.warning("decode error")
#                break
#            else:
#                if 'executable' in queue_info and 'number' in queue_info['executable']:
#                    build_number = str(queue_info['executable']['number'])
#                    log.debug("got build number %s" % build_number)
#                    return build_number
#
#                time.sleep(settings.QUEUE_POLL_WAIT)
#                max_wait -= settings.QUEUE_POLL_WAIT
#                if max_wait < 0:
#                    log.error("max poll limit reached (%s seconds) for queue item %s!" % (
#                        settings.QUEUE_POLL_MAX_WAIT, self.queue_id)
#                    )
#                    break
#
#    def poll_for_completion(self):
#        """Wait for a build to run to completion.
#
#        Make a build api request each ``BUILD_POLL_WAIT`` seconds until a response
#        indicating completion is received, or ``BUILD_POLL_MAX_WAIT`` seconds is reached.
#        """
#        max_wait = settings.BUILD_POLL_MAX_WAIT
#        log.debug('polling build %s, waiting for completion' % self.build_number)
#        while True:
#            try:
#                response = self.session.get(
#                    "%s/job/%s/%s/api/json" % (self.jenkins.host, self.job_name, self.build_number)
#                )
#                response_data = json.loads(response.content)
#            except HTTPError as e:
#                log.error("polling error %s - bailing" % str(e))
#                raise BuildError("http error while polling %s" % str(e))
#            except JSONDecodeError:
#                log.error("Error decoding")
#                raise BuildError("decode error")
#            else:
#                result = BuildResult.from_blob(response_data)
#
#                if not result.building:
#                    log.debug("job has completed")
#                    return result
#
#                log.debug("build %s still running; waiting %s sec" % (
#                    self.build_number, settings.BUILD_POLL_WAIT)
#                )
#                time.sleep(settings.BUILD_POLL_WAIT)
#
#                max_wait -= settings.BUILD_POLL_WAIT
#                if max_wait < 0:
#                    log.error("max poll limit reached (%s seconds) for build %s!" % (
#                        settings.BUILD_POLL_MAX_WAIT, self.build_number)
#                    )
#                    raise BuildError("polled too long")
#
#    @property
#    def url(self):
#        return "%s/job/%s/%s/" % (self.jenkins.host, self.job_name, self.build_number)
#
#    @property
#    def console_url(self):
#        return "%s/job/%s/%s/console" % (self.jenkins.host, self.job_name, self.build_number)
#
#    def __str__(self):
#        return vars(self.__dict__)
#
##
## class JobStatus(Enum):
##     building = 1
##     aborted = 2
##     succeeded = 3
##     failed = 4
##     unstable = 5
##
## job_status = {
##     None: JobStatus.building,
##     "ABORTED": JobStatus.aborted,
##     "SUCCESS": JobStatus.succeeded,
##     "FAILURE": JobStatus.failed,
##     "UNSTABLE": JobStatus.unstable
## }
#
#class BuildResult(object):
#    """Encapsulate results of build."""
#    def __init__(self):
#        self.status = None
#        self.duration = None
#
#    @classmethod
#    def from_blob(cls, blob):
#        ji = BuildResult()
#        if bool(blob['building']):
#            ji.status = JobStatus.building
#        else:
#            ji.status = job_status[blob['result']]
#        ji.duration = timedelta(milliseconds=blob['duration'])
#        return ji
#
#    @property
#    def building(self):
#        return self.status == JobStatus.building
#
#    def __str__(self):
#        return "Status: %s, duration: %s" % (repr(self.status), self.duration)
