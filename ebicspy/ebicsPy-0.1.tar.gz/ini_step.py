#!/usr/bin/python  
# -*- coding: utf-8 -*-

import zlib
import binascii
import os
from httpsEngine import *
from tools import *
from Crypto.PublicKey import RSA
from crypto_tools import *

def ini_exchange(partner, bank):
    httpsEngine = HTTPSEngine(partner, bank)
    ini_request_xml = iniRequest(partner, bank) 
    ini_response = httpsEngine.send(ini_request_xml)
    return check_iniResponse(ini_response)

def ini_orderData(partner):
    #while len(signModulus_str)%8 != 0: #or while len(signModulus_str) < 512
    #    signModulus_str = str(0) + signModulus_str

    signModulus = getattr(partner.getSignPublicKey().key, 'n')
    signExponent = getattr(partner.getSignPublicKey().key, 'e')
    # FIXME : French banks care only about the X509Note. So I don't know if the Modulus and PublicExponent are right encoded...
    # FIXME : why can't we use the same function to encode Modulus and Exponent ?
    signModulus_base64 = binascii.unhexlify(str(hex(signModulus))[2:-1]).encode('base64')
    signExponent_base64 = str(pack_bigint(signExponent)).encode('base64')

    print "############################"
    print long(binascii.hexlify(signModulus_base64.decode('base64')), 16) == signModulus
    print long(binascii.hexlify(signExponent_base64.decode('base64')), 16) == signExponent
    print "############################"

    res = '<?xml version="1.0" encoding="UTF-8"?>\n'
    res += '<SignaturePubKeyOrderData xmlns="http://www.ebics.org/S001" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xsi:schemaLocation="http://www.ebics.org/S001 http://www.ebics.org/S001/ebics_signature.xsd">\n'
    res += '  <SignaturePubKeyInfo>\n'
    if partner.getSignCertificate() != None:
        res += '    <ds:X509Data>\n'
        res += '      <ds:X509IssuerSerial>\n'
        # TODO : read the CN in the certificate
        res += '        <ds:X509IssuerName>'+'CN=ebicspy'+'</ds:X509IssuerName>\n'
        res += '        <ds:X509SerialNumber>'+'01'+'</ds:X509SerialNumber>\n'
        res += '      </ds:X509IssuerSerial>\n'
        # TODO : good format ?
        res += '      <ds:X509Certificate>'+partner.getSignCertificate()+'</ds:X509Certificate>\n'
        res += '    </ds:X509Data>\n'
    res += '    <PubKeyValue>\n'
    res += '      <ds:RSAKeyValue>\n'
    res += '        <ds:Modulus>'+signModulus_base64+'</ds:Modulus>\n'
#    res += '        <ds:Modulus>123</ds:Modulus>\n'
    res += '        <ds:Exponent>'+signExponent_base64+'</ds:Exponent>\n'
    res += '      </ds:RSAKeyValue>\n'
    res += '      <TimeStamp>'+get_timestamp()+'</TimeStamp>\n'
    res += '    </PubKeyValue>\n'
    res += '    <SignatureVersion>A005</SignatureVersion>\n'
    res += '  </SignaturePubKeyInfo>\n'
    res += '  <PartnerID>'+partner.getPartnerId()+'</PartnerID>\n'
    res += '  <UserID>'+partner.getUserId()+'</UserID>\n'
    res += '</SignaturePubKeyOrderData>'

    validateXML(res)
    return res

def iniRequest(partner, bank):
    res = '<?xml version="1.0" encoding="UTF-8"?>\n'
    res += '<ebicsUnsecuredRequest xmlns="http://www.ebics.org/'+EBICS_VERSION+'" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" Revision="'+EBICS_REVISION+'" Version="'+EBICS_VERSION+'" xsi:schemaLocation="http://www.ebics.org/'+EBICS_VERSION+' http://www.ebics.org/'+EBICS_VERSION+'/ebics_keymgmt_request.xsd">\n'
    res += '  <header authenticate="true">\n'
    res += '    <static>\n'
    res += '      <HostID>'+bank.getHostId()+'</HostID>\n'
    res += '      <PartnerID>'+partner.getPartnerId()+'</PartnerID>\n'
    res += '      <UserID>'+partner.getUserId()+'</UserID>\n'
    res += '      <OrderDetails>\n'
    res += '        <OrderType>INI</OrderType>\n'
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
    res += '      <OrderData>'+zlib.compress(ini_orderData(partner), 9).encode('base64')+'</OrderData>\n'
    res += '    </DataTransfer>\n'
    res += '  </body>\n'
    res += '</ebicsUnsecuredRequest>'

    validateXML(res)
    return res

def check_iniResponse(response):
    if response.find('<ReturnCode>000000</ReturnCode>') == -1:
        return False
    return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
