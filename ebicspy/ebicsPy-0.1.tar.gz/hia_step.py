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

import zlib
import binascii
import os
from httpsEngine import *
from tools import *
from Crypto.PublicKey import RSA
from crypto_tools import *

def hia_exchange(partner, bank):
    httpsEngine = HTTPSEngine(partner, bank)
    hia_request_xml = hiaRequest(partner, bank) 
    hia_response = httpsEngine.send(hia_request_xml)
    return check_hiaResponse(hia_response)


def hia_orderData(partner) :
    authModulus = getattr(partner.getAuthPublicKey().key, 'n')
    authExponent = getattr(partner.getAuthPublicKey().key, 'e')
    # FIXME : French banks care only about the X509Note. So I don't know if the Modulus and PublicExponent are right encoded...
    # FIXME : why can't we use the same function to encode Modulus and Exponent ?
    authModulus_base64 = binascii.unhexlify(str(hex(authModulus))[2:-1]).encode('base64')
    authExponent_base64 = str(pack_bigint(authExponent)).encode('base64')

    encryptModulus = getattr(partner.getEncryptPublicKey().key, 'n')
    encryptExponent = getattr(partner.getEncryptPublicKey().key, 'e')
    # FIXME : French banks care only about the X509Note. So I don't know if the Modulus and PublicExponent are right encoded...
    # FIXME : why can't we use the same function to encode Modulus and Exponent ?
    encryptModulus_base64 = binascii.unhexlify(str(hex(encryptModulus))[2:-1]).encode('base64')
    encryptExponent_base64 = str(pack_bigint(encryptExponent)).encode('base64')

    print "############################"
    print long(binascii.hexlify(authModulus_base64.decode('base64')), 16) == authModulus
    print long(binascii.hexlify(authExponent_base64.decode('base64')), 16) == authExponent
    print long(binascii.hexlify(encryptModulus_base64.decode('base64')), 16) == encryptModulus
    print long(binascii.hexlify(encryptExponent_base64.decode('base64')), 16) == encryptExponent
    print "############################"

    res = '<?xml version="1.0" encoding="UTF-8"?>\n'
    res +='<HIARequestOrderData xmlns="http://www.ebics.org/'+EBICS_VERSION+'" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xsi:schemaLocation="http://www.ebics.org/'+EBICS_VERSION+' http://www.ebics.org/'+EBICS_VERSION+'/ebics_orders.xsd">\n'
    res +='  <AuthenticationPubKeyInfo>\n'
    if partner.getAuthCertificate() != None:
          res += '    <ds:X509Data>\n'
          res += '      <ds:X509IssuerSerial>\n'
        # TODO : read the CN in the certificate
          res += '        <ds:X509IssuerName>'+'CN=ebicspy'+'</ds:X509IssuerName>\n'
          res += '        <ds:X509SerialNumber>'+'01'+'</ds:X509SerialNumber>\n'
          res += '      </ds:X509IssuerSerial>\n'
        # TODO : good format ?
          res += '      <ds:X509Certificate>'+partner.getAuthCertificate()+'</ds:X509Certificate>\n'
          res += '    </ds:X509Data>\n'
    res += '    <PubKeyValue>\n'
    res += '      <ds:RSAKeyValue>\n'
    res += '        <ds:Modulus>'+authModulus_base64+'</ds:Modulus>\n'
    res += '        <ds:Exponent>'+authExponent_base64+'</ds:Exponent>\n'
    res += '      </ds:RSAKeyValue>\n'
    res += '    </PubKeyValue>\n'
    res += '    <AuthenticationVersion>X002</AuthenticationVersion>\n'
    res += '  </AuthenticationPubKeyInfo>\n'
    res += '  <EncryptionPubKeyInfo>\n'
    if partner.getEncryptCertificate() != None:
          res += '    <ds:X509Data>\n'
          res += '      <ds:X509IssuerSerial>\n'
        # TODO : read the CN in the certificate
          res += '        <ds:X509IssuerName>'+'CN=ebicspy'+'</ds:X509IssuerName>\n'
          res += '        <ds:X509SerialNumber>'+'01'+'</ds:X509SerialNumber>\n'
          res += '      </ds:X509IssuerSerial>\n'
        # TODO : good format ?
          res += '      <ds:X509Certificate>'+partner.getEncryptCertificate()+'</ds:X509Certificate>\n'
          res += '    </ds:X509Data>\n'
    res += '    <PubKeyValue>\n'
    res += '      <ds:RSAKeyValue>\n'
    res += '        <ds:Modulus>'+encryptModulus_base64+'</ds:Modulus>\n'
    res += '        <ds:Exponent>'+encryptExponent_base64+'</ds:Exponent>\n'
    res += '      </ds:RSAKeyValue>\n'
    res += '    </PubKeyValue>\n'
    res += '    <EncryptionVersion>E002</EncryptionVersion>\n'
    res += '  </EncryptionPubKeyInfo>\n'
    res += '  <PartnerID>'+partner.getPartnerId()+'</PartnerID>\n'
    res += '  <UserID>'+partner.getUserId()+'</UserID>\n'
    res += '</HIARequestOrderData>'

    validateXML(res)
    return res

def hiaRequest(partner, bank) :
    res = '<?xml version="1.0" encoding="UTF-8"?>\n'
    res += '<ebicsUnsecuredRequest xmlns="http://www.ebics.org/'+EBICS_VERSION+'" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" Revision="'+EBICS_REVISION+'" Version="'+EBICS_VERSION+'" xsi:schemaLocation="http://www.ebics.org/'+EBICS_VERSION+' http://www.ebics.org/'+EBICS_VERSION+'/ebics_keymgmt_request.xsd">\n'
    res += '  <header authenticate="true">\n'
    res += '    <static>\n'
    res += '      <HostID>'+bank.getHostId()+'</HostID>\n'
    res += '      <PartnerID>'+partner.getPartnerId()+'</PartnerID>\n'
    res += '      <UserID>'+partner.getUserId()+'</UserID>\n'
    res += '      <OrderDetails>\n'
    res += '        <OrderType>HIA</OrderType>\n'
    if EBICS_VERSION == 'H003':
        res += '        <OrderID>A00A</OrderID>\n'
    res += '        <OrderAttribute>DZNNN</OrderAttribute>\n'
    res += '      </OrderDetails>\n'
    res += '      <SecurityMedium>0000</SecurityMedium>\n'
    res += '    </static>\n'
    res += '    <mutable/>\n'
    res += '  </header>\n'
    res += '  <body>\n'
    res += '    <DataTransfer>\n'
    res += '      <OrderData>'+zlib.compress(hia_orderData(partner), 9).encode('base64')+'</OrderData>\n'
    res += '    </DataTransfer>\n'
    res += '  </body>\n'
    res += '</ebicsUnsecuredRequest>'

    validateXML(res)
    return res

def check_hiaResponse(response):
    if response.find('<ReturnCode>000000</ReturnCode>') == -1:
        return False
    return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
