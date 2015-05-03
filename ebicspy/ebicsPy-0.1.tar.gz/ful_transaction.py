# -*- coding: utf-8 -*-
#############################################################################
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

import re
import zlib
import binascii
import os
from os.path import exists, join
import hashlib
import array
from httpsEngine import *
from tools import *
from Crypto import Random
from crypto_tools import *
from Crypto.PublicKey import RSA
import time as T
import datetime
from Crypto.Cipher import AES
from readOrderDataResponse import *
from Crypto.Signature import PKCS1_v1_5
import StringIO
from base64 import b64encode, b64decode
from tools import *
from datetime import date, time, datetime
from Crypto.Hash import SHA256

def fileUpload_from_fileSystem(partner, bank, file_path, file_format, file_name, test_mode):
    file_content =  open(file_path, "rb").read()
    return fileUpload(partner, bank, file_content, file_format, file_name, test_mode)

def fileUpload(partner, bank, file_content, file_format, file_name, test_mode):
    #TODO check the file_format : only DirectDebit and CreditTransfert ISO20022 formats
    #escape file_name


    aes_key = binascii.hexlify(os.urandom(16)).upper()

    segment_list = get_file_compressed_encrypted_base64_splited(file_content, MAX_ORDER_DATA_LENGTH, aes_key)
    segment_total = len(segment_list)

    httpsEngine = HTTPSEngine(partner, bank)
    ful_initRequest_xml = ful_initResquest(partner, bank, file_content, segment_total, aes_key, file_format, file_name, test_mode)
    ful_initResponse = httpsEngine.send(ful_initRequest_xml)
    T.sleep(2) #TODO : remove sleep
    transactionId = read_ful_initResponse(ful_initResponse)

    if transactionId != False :
        for i in range(segment_total):
            segment_number = i+1
            print "======================= WILL SEND SEGMENT number "+str(segment_number)+" of "+str(segment_total)+" ===================="
            segment = segment_list[i]
            attemps = 0
            check = False
            while (check == False and attemps < MAX_ATTEMP_NUMBER):
                ful_transferRequest_xml = ful_transferResquest(partner, bank, transactionId, segment, segment_number, segment_total)
                ful_transfertResponse = httpsEngine.send(ful_transferRequest_xml)
                T.sleep(2)
                check = read_ful_transferResponse(ful_transfertResponse, transactionId, segment_number)
                attemps += 1
            if check == False:
                # MAX_ATTEMP_NUMBER reached
                print "FAIL"
                break
     
    print "YOUR FILE HAS BEEN SENT"
    if partner.getEbicsProfile() == "T" :
        print "YOU USE AN EBICS T PROFILE. YOU HAVE TO CONFIRM YOUR ORDER WITH A DISJOINED SIGNATURE TO YOUR BANK USING AN OTHER CANAL (EMAIL, FAX, PHONE, WEBSERVICE...)."
        print "YOUR ORDER WILL NOT BE EXECUTED UNTIL YOU SEND THIS SIGNATURE."

def ful_initResquest(partner, bank, file_content, segment_number, aes_key, file_format, file_name, test_mode):
    nonce = binascii.hexlify(os.urandom(16)).upper()
    time_value = get_timestamp()

    aes_key_encrypted_base64 = encrypt_aes_key(aes_key, bank)
    orderData_signature_compressed_encrypted_aes_base64 =  get_compressed_cryptedAES_base64_OrderData_signature(file_content, partner, aes_key)

    bank_auth_hash = bank.getKeyHash(bank.getAuthKey())
    bank_encrypt_hash = bank.getKeyHash(bank.getEncryptKey())

    header = '  <header authenticate="true">\n'
    header += '    <static>\n'
    header += '      <HostID>'+bank.getHostId()+'</HostID>\n'
    header += '      <Nonce>'+nonce+'</Nonce>\n'
    header += '      <Timestamp>'+time_value+'</Timestamp>\n'
    header += '      <PartnerID>'+partner.getPartnerId()+'</PartnerID>\n'
    header += '      <UserID>'+partner.getUserId()+'</UserID>\n'
    header += '      <Product Language="fr">'+PRODUCT_VERSION+'</Product>\n'
    header += '      <OrderDetails>\n'
    header += '        <OrderType>FUL</OrderType>\n'
# (Conditional) OrderID is only present if a file is transmitted to the bank relating to an order with an already existing order number
    header += '        <OrderID>'+get_orderID()+'</OrderID>\n'
    #FIXME : orderAttribute = OZHNN if we are using EBICS TS French profile
    header += '        <OrderAttribute>DZHNN</OrderAttribute>\n'
#    header += '        <FULOrderParams>\n'
#    header += '        <FULOrderParams xmlns:h003="http://www.ebics.org/H003" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="h003:FULOrderParamsType">\n'
    header += '        <FULOrderParams xsi:type="h003:FULOrderParamsType" xmlns:h003="http://www.ebics.org/H003" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n'
    #header += '          <Parameter>\n'
    #header += '            <Name>'+file_name+'</Name>\n'
    #header += '            <Value Type="string">true</Value>\n'
    #header += '          </Parameter>\n'
    if test_mode == True :
        header += '          <Parameter>\n'
        header += '            <Name>TEST</Name>\n'
        header += '            <Value Type="string">true</Value>\n'
        header += '          </Parameter>\n'
    header += '          <FileFormat CountryCode="FR">'+file_format+'</FileFormat>\n'
    header += '        </FULOrderParams>\n'
   # header += '       <StandardOrderParams/>\n'
    header += '      </OrderDetails>\n'
    header += '      <BankPubKeyDigests>\n'
    header += '        <Authentication Version="X002" Algorithm="http://www.w3.org/2001/04/xmlenc#sha256">'+bank_auth_hash+'</Authentication>\n'
    header += '        <Encryption Version="E002" Algorithm="http://www.w3.org/2001/04/xmlenc#sha256">'+bank_encrypt_hash+'</Encryption>\n'
    header += '      </BankPubKeyDigests>\n'
    header += '      <SecurityMedium>0000</SecurityMedium>\n'
    header += '      <NumSegments>'+str(segment_number)+'</NumSegments>\n'
    header += '    </static>\n'
    header += '    <mutable>\n'
    header += '      <TransactionPhase>Initialisation</TransactionPhase>\n'
    header += '    </mutable>\n'
    header += '  </header>'

    data_encryption_info =  '      <DataEncryptionInfo authenticate="true">\n'
    data_encryption_info += '        <EncryptionPubKeyDigest Version="E002" Algorithm="http://www.w3.org/2001/04/xmlenc#sha256">'+bank_encrypt_hash+'</EncryptionPubKeyDigest>\n'
    data_encryption_info += '        <TransactionKey>'+aes_key_encrypted_base64+'</TransactionKey>\n'
    data_encryption_info += '      </DataEncryptionInfo>'

    signature_data = '      <SignatureData authenticate="true">'+orderData_signature_compressed_encrypted_aes_base64+'</SignatureData>'
 

    res = '<?xml version="1.0" encoding="UTF-8"?>\n'
    res += '<ebicsRequest xmlns="http://www.ebics.org/H003" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" Revision="1" Version="H003">\n'
    res += header+'\n'
    res += '  <AuthSignature/>\n'
    res += '  <body>\n'
    res += '    <DataTransfer>\n'
    res += data_encryption_info+'\n'
    res += signature_data+'\n'
    res += '    </DataTransfer>\n'
    res += '  </body>\n'
    res += '</ebicsRequest>'

    auth_signature = get_AuthSignature_node(partner.getAuthPrivateKey(), res)
    res = res.replace('<AuthSignature/>', auth_signature)

    validateXML(res)
    return res
    
def read_ful_initResponse(response):
    #if check_orderDataResponse(response) == False:
    #    return False
    #if chech_xml_AuthSignature == False :
    #    return False

    response = re.sub('xmlns="[^"]+"', '', response) 
    response = re.sub('ds:', '', response) #FIXME : peut-il y avoir cette séquence dans une chaine Base64 ? 
    response = re.sub('xmlns="http://www.ebics.org/H003"', '', response) 

    root = etree.fromstring(response)
    transactionId = root.xpath("//header/static/TransactionID/text()")[0]
    return transactionId

def ful_transferResquest(partner, bank, transactionId, file_segment_compressed_encrypted_base64, segment_number, segment_total):
    #header = '  <header authenticate="true">\n'
    header = '  <header xmlns="http://www.ebics.org/H003" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" authenticate="true">'
    header += '    <static>\n'
    header += '      <HostID>'+bank.getHostId()+'</HostID>\n'
    header += '      <TransactionID>'+transactionId+'</TransactionID>\n'
    header += '    </static>\n'
    header += '    <mutable>\n'
    header += '      <TransactionPhase>Transfer</TransactionPhase>\n'
    header += '      <SegmentNumber>'+str(segment_number)+'</SegmentNumber>\n'
    header += '    </mutable>\n'
    header += '  </header>'

    res = '<?xml version="1.0" encoding="UTF-8"?>\n'
    res += '<ebicsRequest xmlns="http://www.ebics.org/H003" Revision="1" Version="H003">\n'
    res += header+'\n'
    res += '<AuthSignature/>\n'
    res += '  <body>\n'
    res += '    <DataTransfer>\n'
    res += '      <OrderData>'+file_segment_compressed_encrypted_base64+'</OrderData>\n'
    res += '    </DataTransfer>\n'
    res += '  </body>\n'
    res += '</ebicsRequest>'

    if segment_number == segment_total :
        res = res.replace('<SegmentNumber>', '<SegmentNumber lastSegment="true">')
    auth_signature = get_AuthSignature_node(partner.getAuthPrivateKey(), res)
    res = res.replace('<AuthSignature/>', auth_signature)

    res = res.replace('<ebicsRequest xmlns="http://www.ebics.org/H003" Revision="1" Version="H003">', '<ebicsRequest xmlns="http://www.ebics.org/H003" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" Revision="1" Version="H003">')

    validateXML(res)
    return res
    

def read_ful_transferResponse(response, transactionId, segment_number):
    response = re.sub('xmlns="[^"]+"', '', response) 
    response = re.sub('ds:', '', response) #FIXME : peut-il y avoir cette séquence dans une chaine Base64 ? 
    response = re.sub('xmlns="http://www.ebics.org/H003"', '', response) 
    root = etree.fromstring(response)
    #transactionId_response = root.xpath("//header/static/TransactionID/text()")[0]
    #if transactionId_response != transactionID:
    #    return False
    #segment_number_response = root.xpath("//header/mutable/SegmentNumber/text()")[0]
    #if segment_number_response != segment_number: 
    #    return False
    #if check_orderDataResponse(response) == False:
    #    return False
    #if chech_xml_AuthSignature == False :
    #    return False
    return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
