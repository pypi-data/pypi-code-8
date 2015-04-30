import os
import mimetypes
import logging
import base64
import requests

log = logging.getLogger("bq.http_client")

def request(url, method="GET", body=None, headers = None,
            async=False, callback=None, client=None, **kw):
    """Create an http  request

    :param url:  The url for the request
    :param method: GET, PUT, POST, HEAD, DELETE
    :param body: body of post or put (maybe string, file or iterable)
    :param async:
    :rtype response_headers, content
    """
    headers = headers or {}
    userpass = kw.pop('userpass', None)
    if userpass and 'authorization' not in headers:
        headers['authorization'] =  'Basic ' + base64.encodestring("%s:%s" % userpass ).strip()
    response = requests.request (method=method, url=url, data=body, headers=headers, verify=False)
    return response.headers, response.content


def xmlrequest(url, method="GET", body=None, headers=None, **kw):
    headers['content-type'] = 'text/xml'
    return request(url, method=method, body=body, headers=headers, **kw)


def local_request(url, method="GET", body=None, headers=None, **kw):
    """Send a request to the local application
    and return a webob response
    """
    from pyramid.threadlocal import get_current_request
    from pyramid.request import Request
    request = get_current_request()
    if request:
        return request.invoke_subrequest (Request.blank (url))
    return None


def post_files (url,  fields = None, **kw):
    """
    Post fields and files to an http host as multipart/form-data.
    fields is a sequence of (name, value) elements for regular form
    fields.  files is a sequence of (name, filename, value) elements
    for data to be uploaded as files
    Return the tuple (rsponse headers, server's response page)

    example:
      post_files ('http://..',
      fields = {'file1': open('file.jpg','rb'), 'name':'file' })
      post_files ('http://..', fields = [('file1', 'file.jpg', buffer), ('f1', 'v1' )] )
    """


    #body, headers = encode.multipart_encode(fields)
    response =  request(method='POST', url=url, headers=headers, files = fields)
    return response.headers, response.content

def get_file (url, path = None):
    if path == None:
        from tempfile import NamedTemporaryFile
        f = NamedTemporaryFile(delete=False)
    else:
        f = open(path, 'wb')

    headers, content = request(url=url)
    f.write (content)
    f.close()
    return f.name


####################

def send (req):
    'Send a webob request and return a webresponse object'

    from webob import Response

    resp = requests.request (method = req.method,
                             url = req.url,
                             headers = req.headers,
                             data = req.body,
                             verify=False)
    #headers, content = request(req.url,
    #                        method = req.method,
    #                        headers = req.headers,
    #                        body = req.body)

    response = Response()
    response.status = resp.status_code
    response.headers = resp.headers
    response.body    = resp.content
    return response
