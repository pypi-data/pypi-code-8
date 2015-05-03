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

import re
import zlib
import uuid
import binascii
import os
import hashlib
import array
from httpsEngine import *
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from tools import *
from crypto_tools import *
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from readOrderDataResponse import *
import StringIO
from base64 import b64encode, b64decode

def fileDownload_to_fileSystem(partner, bank, destination_path, start_date=None, end_date=None, fdl_type='camt.xxx.cfonb120.stm'):
    file_content = fileDownload(partner, bank , start_date, end_date, fdl_type)
    f = open(join(destination_path, str(uuid.uuid1())) , "w")
    f.write(file_content)
    f.close()

def fileDownload(partner, bank, start_date=None, end_date=None, fdl_type='camt.xxx.cfonb120.stm'):
    httpsEngine = HTTPSEngine(partner, bank)
    fdl_initRequest_xml = fdl_initResquest(partner, bank, fdl_type, start_date, end_date)
    fdl_initResponse = httpsEngine.send(fdl_initRequest_xml)
    transactionId, segment_number, numSegments, sent_file_signature, encryptedTransactionKey, segment, encryptionPubKeyDigest, hostId = read_fdl_initResponse(fdl_initResponse, bank)
    
    segment_list = []
    segment_list.append(segment)

    aes_key = decrypt_aes_key(encryptedTransactionKey, partner)
    

    if transactionId != False :
        # fdl_ini_response is always the first download segment
        # the first segement sent by fdl_transferRequest is number 2
        # TODO : check that the first was the fdl_iniResponse segmentNumber(it's odd, that's not the same upload logic)
        while (segment_number < numSegments) :
            fdl_transferRequest_xml = fdl_transferResquest(partner, bank, transactionId, segment_number)
            fdl_transferResponse = httpsEngine.send(fdl_transferRequest_xml)
            check, last_segment, segment = read_fdl_transfertResponse(fdl_transfertResponse, transactionId, segment_number, bank)
            if check == True:
                segment_list.append(segment)
                segment_number =+ 1
            # TODO : should we test last_segment and exit if True ? => redondance with the while condition

    file_signature = None
    check, file_content = gather_decode_decrypt_decompress(segment_list, file_signature, bank, aes_key)

    if check != True :
        print " ================= ERROR WHILE SIGNATURE VERIFICATION ================="

    #TODO : ckeck aknowledgement
    fdl_acknowledgementRequest_xml = fdl_acknowledgementRequest(partner, bank, transactionId, 0)
    fdl_acknoledgementResponse = httpsEngine.send(fdl_acknowledgementRequest_xml)
    #check = read_fdl_acknowledgementResponse(fdl_transfertResponse) # renvoyer l'acknoledgement tant que ckeck est != True ? => NON !
    
    return file_content

def fdl_initResquest(partner, bank, fdl_type, start_date=None, end_date=None):
    nonce = binascii.hexlify(os.urandom(16)).upper()
    time_value = get_timestamp()

    bank_auth_hash = bank.getKeyHash(bank.getAuthKey())
    bank_encrypt_hash = bank.getKeyHash(bank.getEncryptKey())

    fdl_type = "pain.xxx.cfonb160.dct"

    #TODO : FDL doesn't have any date range ? (to get all cash operations in a specific period)
    #FIXME : OrderAttribute  OHZNN or DHZNN or DZNNN ? ==>> make encryption arrangements
    res = '<?xml version="1.0" encoding="UTF-8"?>\n'
#    res += '<ebicsRequest xmlns="http://www.ebics.org/'+EBICS_VERSION+'" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" Revision="'+EBICS_REVISION+'" Version="'+EBICS_VERSION+'">\n'
    res += '<ebicsRequest Revision="1" Version="H003" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns="http://www.ebics.org/H003">\n'
    res += '  <header authenticate="true">\n'
    res += '    <static>\n'
    res += '      <HostID>'+bank.getHostId()+'</HostID>\n'
    res += '      <Nonce>'+nonce+'</Nonce>\n'
    res += '      <Timestamp>'+time_value+'</Timestamp>\n'
    res += '      <PartnerID>'+partner.getPartnerId()+'</PartnerID>\n'
    res += '      <UserID>'+partner.getUserId()+'</UserID>\n'
    res += '      <Product Language="fr">'+PRODUCT_VERSION+'</Product>\n'
    res += '      <OrderDetails>\n'
    res += '        <OrderType>FDL</OrderType>\n'
#    res += '        <OrderID>B00L</OrderID>\n'
    #FIXME : orderAttribute = OZHNN if we are using EBICS TS French profile
    res += '        <OrderAttribute>DZHNN</OrderAttribute>\n'
#    res += '        <StandardOrderParams/>\n'
#    res += '        <FDLOrderParams xmlns:h003="http://www.ebics.org/'+EBICS_VERSION+'" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="h003:FDLOrderParamsType">\n'
    res += '        <FDLOrderParams xsi:type="h003:FDLOrderParamsType" xmlns:h003="http://www.ebics.org/H003" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n'
    if start_date!=None and end_date!=None:
        res += '          <DateRange>\n'
        res += '            <Start>'+start_date+'</Start>\n'
        res += '            <End>'+end_date+'</End>\n'
        res += '          <DateRange>\n'
    res += '          <FileFormat CountryCode="FR">'+fdl_type+'</FileFormat>\n'
    res += '        </FDLOrderParams>\n'
    res += '      </OrderDetails>\n'
    res += '      <BankPubKeyDigests>\n'
    res += '        <Authentication Version="X002" Algorithm="http://www.w3.org/2001/04/xmlenc#sha256">'+bank_auth_hash+'</Authentication>\n'
    res += '        <Encryption Version="E002" Algorithm="http://www.w3.org/2001/04/xmlenc#sha256">'+bank_encrypt_hash+'</Encryption>\n'
    res += '      </BankPubKeyDigests>\n'
    res += '      <SecurityMedium>0000</SecurityMedium>\n'
    res += '    </static>\n'
    res += '    <mutable>\n'
    res += '      <TransactionPhase>Initialisation</TransactionPhase>\n'
    res += '    </mutable>\n'
    res += '  </header>\n'
    res += '  <AuthSignature/>\n'
    res += '  <body />\n'
    res += '</ebicsRequest>'

    auth_signature = get_AuthSignature_node(partner.getAuthPrivateKey(), res)
    res = res.replace('  <AuthSignature/>', auth_signature)
    res = res.replace('<ds:SignedInfo xmlns="http://www.ebics.org/H003" xmlns:ds="http://www.w3.org/2000/09/xmldsig#">', '<ds:SignedInfo>')

    print "EMIS éééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééé"
    check_AuthSignature_node(res, partner)
    print "éééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééé"
    return res
    

 

def read_fdl_initResponse(response, bank):
    print "éééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééé"
    check_AuthSignature_node(response, bank)
    print "éééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééé"

    if check_orderDataResponse(response) == False:
        return False
    #if chech_xml_AuthSignature == False :
    #    return False

    response = re.sub('xmlns="[^"]+"', '', response)
    response = re.sub('ds:', '', response) #FIXME : peut-il y avoir cette séquence dans une chaine Base64 ? 
    response = re.sub('xmlns="http://www.ebics.org/H003"', '', response)

    #check OrderId
    root = etree.fromstring(response)
    transactionId = root.xpath("//header/static/TransactionID/text()")[0]
    #FIXME: if [EBICS_OK] No download data available then noNumSegment leaf
    numSegments = root.xpath("//header/static/NumSegments/text()")[0]

    segment_number_response = root.xpath("//header/mutable/SegmentNumber/text()")[0]
    if int(segment_number_response) != 1: 
        # fdl_ini_response is always the first download segment
        return False

    #TODO : bank's orderData signature is not compulsory ? 
    sent_file_signature = None
    encryptedTransactionKey = root.xpath("//body/DataTransfer/DataEncryptionInfo/TransactionKey/text()")[0]
    first_segment = root.xpath("//body/DataTransfer/OrderData/text()")[0]
    encryptionPubKeyDigest = root.xpath("//body/DataTransfer/DataEncryptionInfo/EncryptionPubKeyDigest/text()")[0]
    hostId = root.xpath("//body/DataTransfer/DataEncryptionInfo/EncryptionPubKeyDigest/text()")[0]
    return transactionId, segment_number_response, numSegments, sent_file_signature, encryptedTransactionKey, first_segment, encryptionPubKeyDigest, hostId


def fdl_transfertResquest(partner, bank, transactionId, segment_number):
    res = '<?xml version="1.0" encoding="UTF-8"?>\n'
   # res += '<ebicsRequest Revision="'+EBICS_REVISION+'" Version="'+EBICS_VERSION+'" xsi:schemaLocation="http://www.ebics.org/'+EBICS_VERSION+' http://www.ebics.org/'+EBICS_VERSION+'/ebics_request.xsd" xmlns="http://www.ebics.org/'+EBICS_VERSION+'" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ds="http://www.w3.org/2000/09/xmldsig#">\n'
    res += '<ebicsRequest xmlns="http://www.ebics.org/H003" Revision="1" Version="H003">\n'
    res += '  <header xmlns="http://www.ebics.org/H003" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" authenticate="true">'
   # res += '  <header authenticate="true">\n'
    res += '    <static>\n'
    res += '      <HostID>'+bank.getHostId()+'</HostID>\n'
    res += '      <TransactionID>'+transactionId+'</TransactionID>\n'
    res += '    </static>\n'
    res += '    <mutable>\n'
    res += '      <TransactionPhase>Transfert</TransactionPhase>\n'
    res += '    </mutable>\n'
    res += '  </header>'
    res += '  <AuthSignature/>\n'
    res += '  <body/>\n'
    res += '</ebicsRequest>'

    auth_signature = get_AuthSignature_node(partner, res)
    res = res.replace('<AuthSignature/>', auth_signature)

    res = res.replace('<ebicsRequest xmlns="http://www.ebics.org/H003" Revision="1" Version="H003">', '<ebicsRequest xmlns="http://www.ebics.org/H003" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" Revision="1" Version="H003">')
    validateXML(res)
    return res

def read_fdl_transfertResponse(response, transactionId, segment_number, bank):

    last_segment = False

    response = re.sub('xmlns="[^"]+"', '', response)
    response = re.sub('ds:', '', response) #FIXME : peut-il y avoir cette séquence dans une chaine Base64 ? 
    response = re.sub('xmlns="http://www.ebics.org/H003"', '', response)

    if response.find('<SegmentNumber lastSegment="true">') != -1:
        last_segment = True
    root = etree.fromstring(response)
    transactionId_responde = root.xpath("//header/static/TransactionID/text()")[0]
    if transactionId_response != transactionID:
        return False
    segment_number_response = root.xpath("//header/mutable/SegmentNumber/text()")[0]
    if segment_number_response != segment_number: 
        return False
    #if chech_xml_AuthSignature == False:
    #    return False
    return check, last_segment, content

def fdl_acknowledgementRequest(partner, bank, transactionId, receipt_code):
    res = '<?xml version="1.0" encoding="UTF-8"?>\n'
    #res += '<ebicsRequest Revision="'+EBICS_REVISION+'" Version="'+EBICS_VERSION+'" xsi:schemaLocation="http://www.ebics.org/'+EBICS_VERSION+' http://www.ebics.org/'+EBICS_VERSION+'/ebics_request.xsd" xmlns="http://www.ebics.org/'+EBICS_VERSION+'" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ds="http://www.w3.org/2000/09/xmldsig#">\n'
    res += '<ebicsRequest xmlns="http://www.ebics.org/H003" Revision="1" Version="H003">\n'
    #res += '  <header authenticate="true">\n'
    res += '  <header xmlns="http://www.ebics.org/H003" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" authenticate="true">\n'
    res += '    <static>\n'
    res += '      <HostID>'+bank.getHostId()+'</HostID>\n'
    res += '      <TransactionID>'+transactionId+'</TransactionID>\n'
    res += '    </static>\n'
    res += '    <mutable>\n'
    res += '      <TransactionPhase>Receipt</TransactionPhase>\n'
    res += '    </mutable>\n'
    res += '  </header>\n'
    res += '  <AuthSignature/>\n'
    res += '  <body>\n'
    res += '    <TransferReceipt xmlns="http://www.ebics.org/H003" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" authenticate="true">\n'
#    res += '    <TransferReceipt authenticate="true">\n'
    res += '      <ReceiptCode>'+str(receipt_code)+'</ReceiptCode>\n'
    res += '    </TransferReceipt>\n'
    res += '  </body>\n'
    res += '</ebicsRequest>' 

    auth_signature = get_AuthSignature_node(partner.getAuthPrivateKey(), res)
    res = res.replace('<AuthSignature/>', auth_signature)
    res = res.replace('<ebicsRequest xmlns="http://www.ebics.org/H003" Revision="1" Version="H003">', '<ebicsRequest xmlns="http://www.ebics.org/H003" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" Revision="1" Version="H003">')
    validateXML(res)

    return res

def read_fdl_acknowledegmentResponse():
    #TODO
    print 'TODO'

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
