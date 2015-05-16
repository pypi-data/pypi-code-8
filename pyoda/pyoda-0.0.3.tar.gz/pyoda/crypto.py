
import types
import hashlib
import base64
import json
import struct
import hmac
import pyoda.request
import keyczar.readers
from Crypto.Cipher import AES
from  Crypto.Protocol.KDF import PBKDF2

def decodeBase64( data ):
  remainder = len(data) % 4
  if remainder:
    if remainder == 1:
      raise pyoda.err.Error( "Incorrect input length for base64 padding" )
    data += '!!=='[remainder:]
  #Some python versions give problems with urlsafe_b64decode
  return base64.b64decode( data.replace( "-", "+" ).replace( "_", "/" ) )

def unpackList( data ):
  nentries = struct.unpack('>L', data[:4] )[0]
  entries = []
  index = 4
  for i in range( nentries ):
    l = struct.unpack('>L', data[index:index+4] )[0]
    index += 4
    entries.append( data[index:index + l] )
    index += l
  return entries


class Key(object):

  def __init__( self, keyObj, passwd = None):
    if type( keyObj ) in types.StringTypes:
      keyObj = json.loads( keyObj )
    self.__keyObj = keyObj
    self.__passwd = passwd
    self.__crypter = None
    self.__signer = None

  def __getReader( self ):
    if not self.__passwd:
      return JsonKeyReader( self.__keyObj )
    return keyczar.readers.EncryptedReader(
        JsonKeyReader( self.__keyObj ),
        KeyDecrypter( self.__passwd ) )

  def __getCrypter( self ):
    if not self.__crypter:
        self.__crypter = keyczar.keyczar.Crypter( self.__getReader() )
    return self.__crypter

  def decryptWithSession( self, b64msg ):
    msg = decodeBase64(b64msg)
    entries = unpackList( msg )
    sess = entries[0]
    if sess[0] != chr(0):
      sess = decodeBase64(sess)
    #Expects base64 data
    plainsess = self.__getCrypter().Decrypt( base64.b64encode( sess ) )
    sesCipher = SessionCipher( plainsess )
    #Fucking codification has a EOT at the end (ASCII 4)
    return sesCipher.decrypt( entries[1] ).strip().strip(chr(4)).strip(chr(15))


class Crypto(object):

  def __init__( self, org, passwd ):
    self.__org = org
    self.__keys = {}
    self.__pass = passwd

  @property
  def keys( self ):
    return len(self.__keys)

  def __authPass( self ):
    return hashlib.sha256( self.__pass + ":login" ).hexdigest()

  def __keyPass( self ):
    return hashlib.sha256( self.__pass + ":key" ).hexdigest()

  def retrieveCSKeys(self):
    if self.__keys:
      return
    payload = { "password" : self.__authPass() }
    self.__keys = pyoda.request.post( self.__org, self.__org.user_url( "/key_pair" ), payload )

  def decryptWithSession(self,b64msg):
    return Key( self.__keys[ "private_encrypt_key" ], self.__keyPass() ).decryptWithSession( b64msg )


class JsonKeyReader(object):

  def __init__( self, keyObj ):
    self.__data = keyObj
    self.__cache = {}

  def GetMetadata(self):
    return self.__data[ "meta" ]

  def GetKey( self, version_number ):
    return self.__data[ str( version_number ) ]

class KeyDecrypter(object):

  def __init__( self, passwd ):
    self.__passwd = passwd

  def Decrypt(self,ciphertext):
    ckey = json.loads( ciphertext )
    if ckey[ "cipher" ] != "AES128":
      raise pyoda.err.Error( "Unsupoorted ciphe {0} in key".format( ckey[ "cipher" ] ) )
    if ckey[ "hmac" ] != "HMAC_SHA1":
      raise pyoda.err.Error( "Unsupoorted hmac {0} in key".format( ckey[ "hmac" ] ) )
    iv = decodeBase64( ckey[ "iv" ] )
    salt = decodeBase64( ckey[ "salt" ] )
    keydata = decodeBase64( ckey[ "key" ] )
    aesKey = PBKDF2( self.__passwd, salt, 16, int( ckey[ "iterationCount" ] ) )
    plainkey = AES.new( aesKey, AES.MODE_CBC, iv ).decrypt( keydata )
    #Fucking codification has a EOT at the end (ASCII 4)
    return plainkey.strip().strip(chr(4))


class SessionCipher(object):

  def __init__( self, sessData ):
    entries = unpackList( sessData )
    self.__aesKey = entries[0]
    self.__hmacKey = entries[1]
    self.__hmacObj = hmac.new( self.__hmacKey, digestmod = hashlib.sha1 )
    #Calculate hash
    hashObj = hashlib.sha1()
    hashObj.update( struct.pack( '>L', len( self.__aesKey ) ) )
    hashObj.update( self.__aesKey )
    hashObj.update( self.__hmacKey )
    self.__keyHash = hashObj.digest()[:4]

  def decrypt( self, msg ):
    if msg[0] != chr(0):
      raise pyoda.err.Error( "Invalid version byte" )
    expKeyHash = msg[1:5]
    unpackedMsg = msg[5:]
    if expKeyHash != self.__keyHash:
      raise pyoda.err.Error( "Keyhashes differ" )
    #20 is disgest_size of sha1
    expHM = msg[-20:]
    self.__hmacObj.update( msg[:-20] )
    msgHM = self.__hmacObj.digest()
    if expHM != msgHM:
      raise pyoda.err.Error( "HMAC does not match" )
    iv = unpackedMsg[:len(self.__aesKey )]
    ciphertext = unpackedMsg[len(self.__aesKey):-20]
    return AES.new( self.__aesKey, AES.MODE_CBC, iv ).decrypt( ciphertext )




