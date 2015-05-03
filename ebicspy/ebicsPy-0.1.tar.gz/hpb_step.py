# -*- coding: utf-8 -*ed_hpbResponse
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

from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
import re
import zlib
import binascii
import os
import hashlib
import array
from httpsEngine import *
from tools import *
from crypto_tools import *
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from readOrderDataResponse import *
import StringIO
from base64 import b64encode, b64decode
from fdl_transaction import *

def hpb_exchange(partner, bank, bank_auth_key_hash, bank_encrypt_key_hash):
    httpsEngine = HTTPSEngine(partner, bank)
    hpb_request_xml = hpbRequest(partner, bank) 
    hpb_response = httpsEngine.send(hpb_request_xml)
    auth_certificate, auth_modulus, auth_exponent, auth_version, encrypt_certificate, encrypt_modulus, encrypt_exponent, encrypt_version = read_hpbResponse(hpb_response, partner, bank)
    validity = check_keys_validity(bank, auth_certificate, encrypt_certificate, bank_auth_key_hash, bank_encrypt_key_hash)
    if validity == True :
        bank.saveKeys(auth_certificate, auth_modulus, auth_exponent, auth_version, encrypt_certificate, encrypt_modulus, encrypt_exponent, encrypt_version)
        bank.setEncryptKey(RSA.construct((long(binascii.hexlify(encrypt_modulus), 16), long(binascii.hexlify(encrypt_exponent), 16))))
        bank.setAuthKey(RSA.construct((long(binascii.hexlify(auth_modulus), 16), long(binascii.hexlify(auth_exponent), 16))))
        print "========== RECEPTION OF THE BANK KEYS AND CERTIFICATES DONE  =========="
        print "########## INITIALISATION DONE ##########"
        print "===>>> YOU CAN NOW EXCHANGE FILES USING FDL AND FUL ORDERS"
   
def check_keys_validity(bank, auth_certificate, encrypt_certificate, bank_auth_key_hash, bank_encrypt_key_hash) :
    res = True
    #TODO : why do we truncate the digest hash ?
    digest = compute_X509cert_hash(auth_certificate)[:len(bank_auth_key_hash)]
    if digest != bank_auth_key_hash :
        res = False
        print "The bank's auth key hash is invalid"

    #TODO : why do we truncate the digest hash ?
    digest = compute_X509cert_hash(encrypt_certificate)[:len(bank_encrypt_key_hash)]
    if digest != bank_encrypt_key_hash :
        res = False
        print "The bank's auth key hash is invalid"

    return res

def hpbRequest(partner, bank):
    nonce = binascii.hexlify(os.urandom(16)).upper()
    time_value = get_timestamp()

    res = '<?xml version="1.0" encoding="UTF-8"?>\n'
    res += '<ebicsNoPubKeyDigestsRequest xmlns="http://www.ebics.org/'+EBICS_VERSION+'" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" Revision="'+EBICS_REVISION+'" Version="'+EBICS_VERSION+'">\n'
    res += '  <header authenticate="true">\n'
    res += '    <static>\n'
    res += '      <HostID>'+bank.getHostId()+'</HostID>\n'
    res += '      <Nonce>'+nonce+'</Nonce>\n'
    res += '      <Timestamp>'+time_value+'</Timestamp>\n'
    res += '      <PartnerID>'+partner.getPartnerId()+'</PartnerID>\n'
    res += '      <UserID>'+partner.getUserId()+'</UserID>\n'
    res += '      <Product Language="fr">'+PRODUCT_VERSION+'</Product>\n'
    res += '      <OrderDetails>\n'
    res += '        <OrderType>HPB</OrderType>\n'
    res += '        <OrderAttribute>DZHNN</OrderAttribute>\n'
    res += '      </OrderDetails>\n'
    res += '      <SecurityMedium>0000</SecurityMedium>\n'
    res += '    </static>\n'
#    res += '    <mutable/>\n'
    res += '    <mutable></mutable>\n'
    res += '  </header>'
    res += '\n'
    res += '  <AuthSignature/>\n'
    res += '  <body/>\n'
    res += '</ebicsNoPubKeyDigestsRequest>'

    auth_signature = get_AuthSignature_node(partner.getAuthPrivateKey(), res)
    res = res.replace('  <AuthSignature/>', auth_signature)

    validateXML(res)
    return res


def read_hpbResponse(response, partner, bank):
#    if check_orderDataResponse(response) != True:
#        return False
    

    response = re.sub('xmlns="[^"]+"', '', response) 
    root = etree.fromstring(response)
    encryptedTransactionKey = root.xpath("//body/DataTransfer/DataEncryptionInfo/TransactionKey/text()")[0]
    encryptionPubKeyDigest = root.xpath("//body/DataTransfer/DataEncryptionInfo/EncryptionPubKeyDigest/text()")[0]

    aes_key = decrypt_aes_key(encryptedTransactionKey, partner)

    segment_list = []
    order_data = root.xpath("//body/DataTransfer/OrderData/text()")[0]
    segment_list.append(order_data)
    check_file_signature, file_content = gather_decode_decrypt_decompress(segment_list, None, bank, aes_key)

    response = re.sub('xmlns="[^"]+"', '', file_content) 
    response = re.sub('ds:', '', response) #FIXME : peut-il y avoir cette séquence dans une chaine Base64 ? 
    response = re.sub('xmlns="http://www.ebics.org/H003"', '', response) 

    root = etree.fromstring(response)

    auth_certificate = root.xpath("//AuthenticationPubKeyInfo/X509Data/X509Certificate/text()")[0]
    auth_version = root.xpath("//AuthenticationPubKeyInfo/AuthenticationVersion/text()")[0]
    auth_modulus_base64 = root.xpath("//AuthenticationPubKeyInfo/PubKeyValue/RSAKeyValue/Modulus/text()")[0]
    auth_modulus = auth_modulus_base64.decode('base64')
    auth_exponent_base64 = root.xpath("//AuthenticationPubKeyInfo/PubKeyValue/RSAKeyValue/Exponent/text()")[0]
    auth_exponent = binascii.hexlify(auth_exponent_base64.decode('base64'))

    encrypt_certificate = root.xpath("//EncryptionPubKeyInfo/X509Data/X509Certificate/text()")[0]
    encrypt_version = root.xpath("//EncryptionPubKeyInfo/EncryptionVersion/text()")[0] 
    encrypt_modulus_base64 = root.xpath("//EncryptionPubKeyInfo/PubKeyValue/RSAKeyValue/Modulus/text()")[0]
    encrypt_modulus = encrypt_modulus_base64.decode('base64')
    encrypt_exponent_base64 = root.xpath("//EncryptionPubKeyInfo/PubKeyValue/RSAKeyValue/Exponent/text()")[0]
    encrypt_exponent = binascii.hexlify(encrypt_exponent_base64.decode('base64')) 

    return auth_certificate, auth_modulus, auth_exponent, auth_version, encrypt_certificate, encrypt_modulus, encrypt_exponent, encrypt_version



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
