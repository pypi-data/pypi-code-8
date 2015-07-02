import urllib2
import urllib
try:
    import simplejson as json
except ImportError:
    import json

"""
Error handler
"""
class DefaultErrorHandler(urllib2.HTTPDefaultErrorHandler):
    def http_error_default(self, req, fp, code, msg, headers):
        result = urllib2.HTTPError(
            req.get_full_url(), code, msg, headers, fp)
        result.status = code
        return result

class BaseException(Exception):
    def __init__(self, **kwargs):
        super(Exception, self).__init__(kwargs)

class InvalidApiKeyException(BaseException):
    pass

class InvalidLatLongException(BaseException):
    pass

class ExceedQuotaException(BaseException):
    pass

"""
Walk score needs more time, check back later
"""
class ScoreBeingCalculatedException(BaseException):
    pass

class InternalServerException(BaseException):
    pass

"""
Your IP is blocked
"""
class IpBlockedException(BaseException):
    pass

class WalkScore:
    apiUrl = 'http://api.walkscore.com/score?format'

    def __init__(self, apiKey, format = 'json'):
        self.apiKey = apiKey
        self.format = format

    def makeRequest(self, address, lat = '', long = ''):
        url = '%s=%s&%s&lat=%s&lon=%s&wsapikey=%s' % (self.apiUrl, self.format, urllib.urlencode({'address': address}), lat, long, self.apiKey)
        request = urllib2.Request(url)
        opener = urllib2.build_opener(DefaultErrorHandler())
        first = opener.open(request)

        first_datastream = first.read()

        # Append caching headers
        request.add_header('If-None-Match', first.headers.get('ETag'))
        request.add_header('If-Modified-Since', first.headers.get('Date'))

        response = opener.open(request)

        # some error handling
        responseStatusCode = response.getcode()

        # jsonify response
        jsonResp = json.load(response)
        jsonRespStatusCode = jsonResp['status']

        # Error handling
        # @see http://www.walkscore.com/professional/api.php
        if responseStatusCode == 200 and jsonRespStatusCode == 40:
            raise InvalidApiKeyException(message="Your API is invalid", raw=jsonResp, status_code=responseStatusCode)

        if responseStatusCode == 200 and jsonRespStatusCode == 2:
            raise ScoreBeingCalculatedException(message="walkscore is unavailable, please try again later", raw=jsonResp, status_code=responseStatusCode)

        if responseStatusCode == 200 and jsonRespStatusCode == 41:
            raise ExceedQuotaException(message="You have exceeded API limit", raw=jsonResp, status_code=responseStatusCode)

        if responseStatusCode == 403 and jsonRespStatusCode == 42:
            raise IpBlockedException(message="Your IP is blocked by WalkScore", raw=jsonResp, status_code=responseStatusCode)

        if responseStatusCode == 404 and jsonRespStatusCode == 30:
            raise InvalidLatLongException(message="Invalid latitude and/or longitude", raw=jsonResp, status_code=responseStatusCode)

        if responseStatusCode == 500 and jsonRespStatusCode == 31:
            raise InternalServerException(message="Walk Score API internal error", raw=jsonResp, status_code=responseStatusCode)

        return jsonResp
