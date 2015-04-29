
import pyoda.host
import pyoda.crypto
import pyoda.request

class Organization(object):

  def __init__(self, name, auth, url = "https://oda.cloudjutsu.com", password = "" ):
    self.__name = name
    self.__auth = auth
    self.__url = url
    self.__crypto = pyoda.crypto.Crypto(self,password)

  @property
  def name(self):
    return self.__name

  def user_url(self, path ):
    return "{0}/api/you/{1}".format( self.__url, path.lstrip("/") )

  def url(self, path):
    return "{0}/organization/{1}/api/{2}".format( self.__url, self.__name, path.lstrip("/") )

  @property
  def auth(self):
    return self.__auth

  @property
  def crypto(self):
    return self.__crypto

  def newHost(self):
    return pyoda.host.Host( self )

  def getHosts(self):
    hosts = []
    for h in pyoda.request.get( self, self.url("host") ):
      hosts.append( pyoda.host.Host( self ) )
      hosts[-1].fillFromDict(h)
    return hosts


  def getHost(self, hid):
    return pyoda.host.Host( self, hid )




