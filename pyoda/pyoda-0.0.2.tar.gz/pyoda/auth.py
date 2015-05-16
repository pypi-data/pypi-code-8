

import hashlib
import hmac
import base64
import datetime

class Auth:

  def __init__( self, user, token ):
    self.__user = user
    self.__token = token

  def getHeaders(self, base = None):
    if not base:
      base = {}
    when = datetime.datetime.utcnow().isoformat("T")+"Z"
    mac = hmac.new(self.__token, "{0}|{1}".format( when, self.__user ), hashlib.sha512)
    hs = {
      "X-When" : when,
      "X-Email" : self.__user,
      "X-Hmac-Sha512" : base64.b64encode( mac.digest() )
    }
    hs.update(base)
    return hs

