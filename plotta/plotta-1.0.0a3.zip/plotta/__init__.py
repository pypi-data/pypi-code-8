import unirest
import time
import socket
import uuid

HOSTNAME = 'localhost'
PORT = 3000
PLOTTA_ENABLED = True

# API endpoint wrappers
def job_new(job_id, name, node):
    payload = {'id': job_id, 'name': name, 'node': node}
    url = "http://{0}:{1}/api/job/new".format(HOSTNAME, PORT)
    return sync_request(url, payload)

def job_stop(job_id):
    payload = {'id': job_id}
    url = "http://{0}:{1}/api/job/stop".format(HOSTNAME, PORT)
    async_request(url, payload)

def stream_new(stream_id, job_id, title, x_name, y_name):
    payload = {'id': stream_id, 'job_id': job_id, 'title': title, 'xName': x_name, 'yName': y_name}
    url = "http://{0}:{1}/api/stream/new".format(HOSTNAME, PORT)
    return sync_request(url, payload)

def append(stream_id, job_id, x, y):
    payload = {'id': stream_id, 'job_id': job_id, 'x': x, 'y': y}
    url = "http://{0}:{1}/api/stream/append".format(HOSTNAME, PORT)
    async_request(url, payload)

def sync_request(url, payload):
    try:
        response = unirest.post(url, headers = {"Accept": "application/json"}, params = payload)
        check_success(response)
        return response
    except Exception, e:
        return None

def async_request(url, payload):
    unirest.post(url, headers = {"Accept": "application/json"}, params = payload, callback = _empty_callback)

def _empty_callback(_):
    pass

def check_success(response):
    if response is None or response.code in [404, 502, 503, 504]:
        # Server offline, disable plotta
        print "Plotta server offline. Disabling Plotta."
        PLOTTA_ENABLED = False
    elif response.code in [400, 405, 406, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 501]:
        raise RuntimeError("Plotta user error ({0}). Message: {1}".format(response.code, response.body))
    elif response.code in [500]:
        raise RuntimeError("Plotta server error ({0}). Message: ".format(response.code, response.body))

class Job():

    def __init__(self, job_name, job_id = None, node_name = None):
        if job_id is None:
            job_id = int(round(time.time()))
        if node_name is None:
            node_name = socket.getfqdn()

        self.job_name = job_name
        self.job_id = job_id
        self.node_name = node_name

    def start(self):
        if PLOTTA_ENABLED:
            job_new(self.job_id, self.job_name, self.node_name)

    def stop(self):
        if PLOTTA_ENABLED:
            job_stop(self.job_id)

    def add_stream(self, title, stream_id=None, x_name="", y_name=""):

        if stream_id is None:
            #Generate a unique ID for this stream
            stream_id = uuid.uuid4()

        stream = Stream(stream_id, self.job_id, title, x_name, y_name)
        stream.start()

        return stream

class Stream():

    def __init__(self, stream_id, job_id, title, x_name, y_name):
        self.stream_id = stream_id
        self.job_id = job_id
        self.title = title
        self.x_name = x_name
        self.y_name = y_name

    def start(self):
        if PLOTTA_ENABLED:
            stream_new(self.stream_id, self.job_id, self.title, self.x_name, self.y_name)

    def append(self, x, y):
        if PLOTTA_ENABLED:
            append(self.stream_id, self.job_id, x, y)
