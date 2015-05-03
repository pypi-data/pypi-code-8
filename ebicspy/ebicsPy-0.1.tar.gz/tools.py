# -*- coding: utf-8 -*-
##############################################################################
#
#    ebicspy, EBICS protocol library
#    Copyright (C) 2013-2014 Aurélien DUMAINE (aurelien.dumaine@free.fr).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from lxml import etree
import time
from time import strftime
from os.path import exists, join, dirname
import binascii
import datetime
from random import randint

global MAX_ATTEMP_NUMBER
MAX_ATTEMP_NUMBER = 3
# In France, self-signed certificates are valid five years (see Annex 4 page 25/26 of the EBICS IG CFONB VF 2.1.4 2012 02 24 - GUF")
global SELF_SIGNED_CERTIFICATE_NB_YEARS_VALIDITY
SELF_SIGNED_CERTIFICATE_NB_YEARS_VALIDITY = 5
global MAX_ORDER_DATA_LENGTH
MAX_ORDER_DATA_LENGTH = 1048576
global AUTH_KEY_LENGTH
AUTH_KEY_LENGTH = 2048
global SIGN_KEY_LENGTH
SIGN_KEY_LENGTH = 2048
global ENCRYPT_KEY_LENGTH
ENCRYPT_KEY_LENGTH = 2048
global PARTNER_SIGN_KEY_VERSION
PARTNER_SIGN_KEY_VERSION = "A005"
global PARTNER_ENCRYPT_KEY_VERSION
PARTNER_ENCRYPT_KEY_VERSION = "E002"
global PARTNER_AUTH_KEY_VERSION
PARTNER_AUTH_KEY_VERSION = "X002"
global EBICS_VERSION
EBICS_VERSION = "H003"
global EBICS_REVISION
EBICS_REVISION = "1"
global PRODUCT_VERSION
#PRODUCT_VERSION = "kopiLeft Dev 1.0"
PRODUCT_VERSION = "EbicsPy 0.1"

def get_overlapped_chunks(textin, chunksize, overlapsize):  
    return [ textin[a:a+chunksize] for a in range(0,len(textin), chunksize-overlapsize)]

def get_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")

def get_orderID():
    return "A" + str(randint(100, 999))

def validateXML(xml):
#    print xml
#    print '====================================='

    if EBICS_VERSION == 'H003' :
        #FIXME : use JOIN to concat schemas_version_H003_EBICS2.4 and ebics.xsd
        schema_root = etree.parse(join(dirname(__file__), 'schemas_version_H003_EBICS2.4/ebics.xsd'))
    else:
        schema_root = etree.parse(join(dirname(__file__), 'schemas_version_H004_EBICS2.5/ebics.xsd'))
    schema = etree.XMLSchema(schema_root)
    parser = etree.XMLParser(schema = schema)
    root = etree.fromstring(xml, parser)

class FileSystemLogger : 
    def __init__(self, path="log"):
        self.path = path
        
    def logMessage(self, level, title, string):
        print title, string
        f = open(join(self.path, title+" - "+level), 'w')
        f.write(string)
        f.close()

class XMLStorageService : 
    def __init__(self, path):
        self.path = path
        if exists(path):  
            self.tree = etree.parse(path)
        else :
           self.tree = etree.parse(join(dirname(__file__), 'XMLStorageService_structure.xml'))

    def __del__(self):
        self.saveXML()
        #FIXME : check Schema complicance before writing

    def saveXML(self):
        self.tree.write(self.path)

    def getStatus(self):
        return self.tree.xpath("/root/status/text()")[0]

    def setStatus(self, status):
        self.tree.xpath("/root/status")[0].text = status
        self.saveXML()

    def getBankAuthKeyHash(self):
        if len(self.tree.xpath("/root/bank/auth/certificate_hash/text()")) == 0 :
            h = raw_input("Please enter the bank's auth key hash : ")
            self.tree.xpath("/root/bank/auth/certificate_hash")[0].text = h
        return self.tree.xpath("/root/bank/auth/certificate_hash/text()")[0]

    def getBankEncryptKeyHash(self):
        if len(self.tree.xpath("/root/bank/encrypt/certificate_hash/text()")) == 0 :
            h = raw_input("Please enter the bank's encrypt key hash : ")
            self.tree.xpath("/root/bank/encrypt/certificate_hash")[0].text = h
        return self.tree.xpath("/root/bank/encrypt/certificate_hash/text()")[0]

    def saveLetter(self, letter, letterType):
        self.tree.xpath("/root/partner/letters/"+letterType)[0].text = letter.encode('base64')
        self.saveXML()

    def saveBankKey(self, keyType, keyVersion, modulus, public_exponent, certificate) :
        self.tree.xpath("/root/bank/"+keyType+"/certificate")[0].text = certificate
        self.tree.xpath("/root/bank/"+keyType+"/modulus")[0].text = str(long(binascii.hexlify(modulus), 16))
        self.tree.xpath("/root/bank/"+keyType+"/public_exponent")[0].text = str(int(public_exponent, 16))
        self.tree.xpath("/root/bank/"+keyType+"/version")[0].text = keyVersion
        self.saveXML()

    def savePartnerKey(self, keyType, keyVersion, modulus, private_exponent, public_exponent, certificate) :
        self.tree.xpath("/root/partner/"+keyType+"/certificate")[0].text = certificate
        self.tree.xpath("/root/partner/"+keyType+"/modulus")[0].text = str(modulus) 
        self.tree.xpath("/root/partner/"+keyType+"/public_exponent")[0].text =  str(public_exponent)
        self.tree.xpath("/root/partner/"+keyType+"/private_exponent")[0].text = str(private_exponent)
        self.tree.xpath("/root/partner/"+keyType+"/version")[0].text = keyVersion
        self.saveXML()
    
    def getPartnerKeyComponent(self, keyComponent, keyType):
        res = self.tree.xpath("/root/partner/"+keyType+"/"+keyComponent+"/text()")[0]
        return long(res)

    def getBankKeyComponent(self, keyComponent, keyType):
        res = self.tree.xpath("//bank/"+keyType+"/"+keyComponent+"/text()")[0]
        return long(res)

    def getPartnerCertificate(self, certificateType):
        return self.tree.xpath("//partner/"+certificateType+"/certificate/text()")[0]

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
