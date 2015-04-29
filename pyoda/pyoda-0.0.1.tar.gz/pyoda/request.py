
import urllib2
import json
import pyoda.err

def post( org, path, payload ):
  try:
    req = urllib2.Request( path ,
                           json.dumps(payload),
                           org.auth.getHeaders( { "Content-Type": "application/json" }) )
    resp = urllib2.urlopen(req).read()
    if len(resp) > 0:
      return json.loads(resp)
  except urllib2.HTTPError, e:
    if e.code == 401:
      raise pyoda.err.Unauthorized("{0} to {1}".format(e,path))
    elif e.code == 400:
      raise pyoda.err.Invalid("{0} to {1} ({2})".format(e,path,e.read()))
    raise pyoda.err.Error("{0} to {1}".format(e,path))
  except ValueError, e:
    raise pyoda.err.Error( "Response doesn't seem to be json: {}".format(e))

def get( org, path ):
  try:
    req = urllib2.Request( path ,
                           headers = org.auth.getHeaders() )
    resp = urllib2.urlopen(req).read()
    if len(resp) > 0:
      return json.loads(resp)
  except urllib2.HTTPError, e:
    if e.code == 401:
      raise pyoda.err.Unauthorized("{0} to {1}".format(e,path))
    elif e.code == 400:
      raise pyoda.err.Invalid("{0} to {1}".format(e,path))
    raise pyoda.err.Error("{0} to {1}".format(e,path))
  except ValueError, e:
    raise pyoda.err.Error( "Response doesn't seem to be json: {}".format(e))
