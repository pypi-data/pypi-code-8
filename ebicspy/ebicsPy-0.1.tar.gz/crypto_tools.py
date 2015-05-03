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
from Crypto.Cipher import AES
from readOrderDataResponse import *
from Crypto.Signature import PKCS1_v1_5
import StringIO
from base64 import b64encode, b64decode
from tools import *
from datetime import date, time, datetime
from Crypto.Hash import SHA256
from Padding import *
from OpenSSL import crypto as OpenSSL_crypto
from socket import gethostname
from Crypto.Cipher import PKCS1_v1_5 as padding_rsa

def pack_bigint(i):
    b = bytearray()
    while i:
        b.append(i & 0xFF)
        i >>= 8
    return b
   
def create_rsa_key(key_length, function, storageService):
    partner_key = OpenSSL_crypto.PKey()
    partner_key.generate_key(OpenSSL_crypto.TYPE_RSA, key_length)

    cert = OpenSSL_crypto.X509()
    cert.get_subject().C = "FR"
    cert.get_subject().ST = "Ile de France"
    cert.get_subject().L = "Paris"
    cert.get_subject().O = "ebicspy"
    cert.get_subject().CN = gethostname()
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(SELF_SIGNED_CERTIFICATE_NB_YEARS_VALIDITY*365*24*60*60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(partner_key)
    cert.sign(partner_key, 'sha256')

    cert_txt = OpenSSL_crypto.dump_certificate(OpenSSL_crypto.FILETYPE_PEM, cert)
    certificate = ""
    for line in cert_txt :
        certificate += line.strip()
    certificate = str(certificate).replace('-----BEGINCERTIFICATE-----', '').replace('-----ENDCERTIFICATE-----', '')

    partner_private_PEM = OpenSSL_crypto.dump_privatekey(OpenSSL_crypto.FILETYPE_PEM, partner_key)
    private = RSA.importKey(partner_private_PEM) 
    public = private.publickey() 
    modulus = getattr(private.key, 'n')
    private_exponent = getattr(private.key, 'd')
    public_exponent = getattr(private.key, 'e')

    if function == "encrypt" :
        keyVersion = PARTNER_ENCRYPT_KEY_VERSION
    elif function == "auth" :
        keyVersion = PARTNER_AUTH_KEY_VERSION
    elif function == "sign":
        keyVersion = PARTNER_SIGN_KEY_VERSION
    storageService.savePartnerKey(function, keyVersion, modulus, private_exponent, public_exponent, certificate)

    return private, public, cert_txt

def decrypt_aes_key(encrypted_aes_key_base64, receiver):
    crypted_key = encrypted_aes_key_base64.decode('base64')
    crypted_key_hex = binascii.hexlify(crypted_key)
    decrypted_key_hex = binascii.hexlify(receiver.getEncryptPrivateKey().decrypt(crypted_key))
    aes_key = decrypted_key_hex[len(decrypted_key_hex)-32:]
    aes_key = binascii.unhexlify(aes_key)
    return aes_key

def encrypt_aes_key(aes_key, receiver):
    #TODO : verify utility of the second argument of encrypt
    aes_hex = binascii.unhexlify(aes_key)
    aes_key_encrypted = padding_rsa.new(receiver.getEncryptKey()).encrypt(aes_hex)
    #aes_key_encrypted = receiver.getEncryptKey().encrypt(aes_hex, '')[0]
    aes_key_encrypted_base64 = b64encode(aes_key_encrypted)
    return  aes_key_encrypted_base64

def get_compressed_cryptedAES_base64_OrderData_signature(order_data_string, partner, aes_key):
    # USED ONLY IN UPLOAD INITIALISATION
    #  Body->DataTransfer->SignatureData du message d'initialisation d'upload
    orderData_signature = get_orderData_signature(order_data_string, partner)
    orderData_signature_compressed = zlib.compress(orderData_signature, 9) 
    toCrypt = appendBitPadding(orderData_signature_compressed)
    #FIXME : the iv paramater on AES cipher intialization is put to \0 : Crypto lib doc says it's nt secure (even if IV should not be secret)   
    #iv = Random.new().read(AES.block_size)
    iv = "\0" * AES.block_size
    orderData_signature_compressed_encrypted_aes = AES.new(binascii.unhexlify(aes_key), AES.MODE_CBC, iv).encrypt(toCrypt)
    orderData_signature_compressed_encrypted_aes_base64 = b64encode(orderData_signature_compressed_encrypted_aes)
    return orderData_signature_compressed_encrypted_aes_base64

def get_file_compressed_encrypted_base64_splited(file_content, MAX_ORDER_DATA_LENGTH, aes_key):
    file_content_compressed = zlib.compress(file_content, 9)  
    file_content_compressed = appendBitPadding(file_content_compressed)
    #FIXME : the iv paramater on AES cipher intialization is put to \0 : Crypto lib doc says it's nt secure (even if IV should not be secret)   
    #iv = Random.new().read(AES.block_size)
    iv = "\0" * AES.block_size
    file_content_compressed_encrypt = AES.new(binascii.unhexlify(aes_key), AES.MODE_CBC, iv).encrypt(file_content_compressed) 
    file_content_compressed_encrypt_base64 = b64encode(file_content_compressed_encrypt)
    segment_list = get_overlapped_chunks(file_content_compressed_encrypt_base64, MAX_ORDER_DATA_LENGTH, 0)
    return segment_list

def gather_decode_decrypt_decompress(segment_list, file_signature, bank, aes_key):
    file_content_compressed_encrypt_base64 = ""
    for segment in segment_list :
        file_content_compressed_encrypt_base64 += segment
    file_content_compressed_encrypt = b64decode(file_content_compressed_encrypt_base64)
    #FIXME : the iv paramater on AES cipher intialization is put to \0 : Crypto lib doc says it's nt secure (even if IV should not be secret)   
    #iv = Random.new().read(AES.block_size)
    iv = "\0" * AES.block_size
    file_content_compressed = AES.new(aes_key, AES.MODE_CBC, iv).decrypt(file_content_compressed_encrypt)
    file_content_compressed_hexa = array.array('B', file_content_compressed)
    file_content = zlib.decompress(file_content_compressed_hexa) 

    #TODO check_file_signature. /!\ this bank's signature is not compulsory
    check_file_signature = True
    return check_file_signature, file_content

def get_orderData_signature(order_data_string, partner):
    # USED ONLY IN UPLOAD INITIALISATION

    order_data_string = order_data_string.replace('\n', '').replace('\r', '').replace(chr(26), '')
    digest = SHA256.new(order_data_string)
    p = PKCS1_v1_5.new(partner.getSignPrivateKey())
    signed_info_digest_with_asn1_prefix_signed = p.sign(digest)
    signed_info_digest_with_asn1_prefix_signed_base64 = b64encode(signed_info_digest_with_asn1_prefix_signed)

    res = '<?xml version="1.0" encoding="UTF-8"?>\n'
    res += '<UserSignatureData xmlns="http://www.ebics.org/S001" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.ebics.org/S001 http://www.ebics.org/S001/ebics_signature.xsd">\n'
    res += '  <OrderSignatureData>\n'
    res += '    <SignatureVersion>A005</SignatureVersion>\n'
    res += '    <SignatureValue>'+signed_info_digest_with_asn1_prefix_signed_base64+'</SignatureValue>\n'
    res += '    <PartnerID>'+partner.getPartnerId()+'</PartnerID>\n'
    res += '    <UserID>'+partner.getUserId()+'</UserID>\n'
    res += '  </OrderSignatureData>\n'
    res += '</UserSignatureData>'

    validateXML(res)
    return res

def get_AuthSignature_node(pKey, xml) :
    root = etree.fromstring(xml)
    auth_true_node_list  = root.xpath("//*[@authenticate='true']")
    string = ""
    for s in auth_true_node_list:
        tmp = etree.tostring(s)
        string += tmp[:tmp.rfind('>')+1]

    string = '<root>'+string+'</root>'

    f = StringIO.StringIO(string)
    root = etree.parse(f)
    output = StringIO.StringIO()
    root.write_c14n(output)
    string = output.getvalue()
    string = string.replace('<root>', '').replace('</root>', '')

    m = hashlib.sha256()
    m.update(string)
    string_digest = m.digest()

    string_digest_encoded = b64encode(string_digest)


    signed_info = '<ds:SignedInfo xmlns="http://www.ebics.org/H003" xmlns:ds="http://www.w3.org/2000/09/xmldsig#">\n'
    signed_info += '      <ds:CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"></ds:CanonicalizationMethod>\n'
    signed_info += '      <ds:SignatureMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"></ds:SignatureMethod>\n'
    signed_info += '      <ds:Reference URI="#xpointer(//*[@authenticate=\'true\'])">\n'
    signed_info += '        <ds:Transforms>\n'
    signed_info += '          <ds:Transform Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"></ds:Transform>\n'
    signed_info += '        </ds:Transforms>\n'
    signed_info += '        <ds:DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256"></ds:DigestMethod>\n'
    signed_info += '        <ds:DigestValue>'+string_digest_encoded+'</ds:DigestValue>\n'
    signed_info += '      </ds:Reference>\n'
    signed_info += '    </ds:SignedInfo>'



    # ATTENTION : if Python throw an exception telling the hash object hasn't OID attribute delete the following file
            #/usr/lib/python2.7/dist-packages/Crypto/Hash/SHA256.so
            # cela permet de recompiler proprement ce script en .pyc de la lib pycrypto

    digest = SHA256.new(signed_info)
    p = PKCS1_v1_5.new(pKey)
    signed_info_digest_with_asn1_prefix_signed = p.sign(digest)
    signed_info_digest_with_asn1_prefix_signed_base64 = b64encode(signed_info_digest_with_asn1_prefix_signed)
        
    res = '  <AuthSignature>\n'
    res += '    '+ signed_info+'\n'
    res += '    <ds:SignatureValue>'+signed_info_digest_with_asn1_prefix_signed_base64+'</ds:SignatureValue>\n'
    res += '  </AuthSignature>'

    return res

def check_AuthSignature_node(xml, bank) :
    #Step1 : get file digest
    root = etree.fromstring(xml)
    auth_true_node_list  = root.xpath("//*[@authenticate='true']")
    string = ""
    for s in auth_true_node_list:
        tmp = etree.tostring(s)
        string += tmp[:tmp.rfind('>')+1]

    string = '<root>'+string+'</root>'

    f = StringIO.StringIO(string)
    root = etree.parse(f)
    output = StringIO.StringIO()
    root.write_c14n(output)
    string = output.getvalue()
    string = string.replace('<root>', '').replace('</root>', '')

    m = hashlib.sha256()
    m.update(string)
    string_digest = m.digest()
    string_digest_encoded = b64encode(string_digest)

    signed_info = '<ds:SignedInfo xmlns="http://www.ebics.org/H003" xmlns:ds="http://www.w3.org/2000/09/xmldsig#">\n'
    signed_info += '      <ds:CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"></ds:CanonicalizationMethod>\n'
    signed_info += '      <ds:SignatureMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"></ds:SignatureMethod>\n'
    signed_info += '      <ds:Reference URI="#xpointer(//*[@authenticate=\'true\'])">\n'
    signed_info += '        <ds:Transforms>\n'
    signed_info += '          <ds:Transform Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"></ds:Transform>\n'
    signed_info += '        </ds:Transforms>\n'
    signed_info += '        <ds:DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256"></ds:DigestMethod>\n'
    signed_info += '        <ds:DigestValue>'+string_digest_encoded+'</ds:DigestValue>\n'
    signed_info += '      </ds:Reference>\n'
    signed_info += '    </ds:SignedInfo>'
    
    #Step2 : compare the file digest end the XML value
    response = xml
    response = re.sub('xmlns="[^"]+"', '', response)
    response = re.sub('ds:', '', response) #FIXME : peut-il y avoir cette séquence dans une chaine Base64 ? 
    response = re.sub('xmlns="http://www.ebics.org/H003"', '', response)
    root = etree.fromstring(response)
    xml_digest = root.xpath("//AuthSignature/SignedInfo/Reference/DigestValue/text()")[0]

    if xml_digest != string_digest_encoded :
        print "ERREUR : LE DIGEST CALCULE N'EST PAS LE MEME QUE CELUI PRESENT DANS LA REPONSE"
    else :
        print "OK : LE DIGEST CALCULE EST LE MEME QUE CELUI PRESENT DANS LA REPONSE"
        
    #Step 3 : verify signed_info encrypted digest and the XML value
    base64_xml_digest_signature = root.xpath("//AuthSignature/SignatureValue/text()")[0]
    xml_digest_signature = b64decode(base64_xml_digest_signature)
    signed_info_digest = SHA256.new(signed_info)
    
 
    verifier = PKCS1_v1_5.new(bank.getAuthKey())
    #res = verifier.verify(signed_info_digest, binascii.hexlify(xml_digest_signature))
    res = verifier.verify(signed_info_digest, xml_digest_signature)
    print "777777777777777777777777777777777777777777777777777777777777"
    if res :
       print "The signature is authentic."
    else:
       print "The signature is not authentic."
    
    print "777777777777777777777777777777777777777777777777777777777777"
    return res

def check_orderData_signature(order_data_string, partner):
    # FOR NOW, BANKS NEVER SIGN THE SEPA FILES THEY SEND
    return True

def letter(letter_type, cert_title, cert, hostId, userId, partnerId):
    d = datetime.now()
    res = "                 Lettre d'initialisation pour "+letter_type+"\n"
    res += "                 ================================\n\n\n"
    res += "Date :          "+datetime.strftime(d, "%d/%m/%Y")+"\n"
    res += "Heure :         "+datetime.strftime(d, "%H:%M:%S")+"\n"
    res += "Destinataire :  "+hostId+"\n"
    res += "ID utilisateur :"+userId+"\n"
    res += "ID client :     "+partnerId+"\n"
    res += "\n\n"
    res += cert_title+"\n\n"
    res += "-----BEGIN CERTIFICATE-----\n"
    tmp = ''
    for i in cert:
        tmp+=i
        if len(tmp) == 77:
            res += tmp+'\n'
            tmp = ''
    if len(tmp) > 0 :
        res += tmp
    res += "\n-----END CERTIFICATE-----\n\n\n"
    res += "Hash du certificat de signature (SHA-256) :\n\n"

    digest = compute_X509cert_hash(cert)

    h_string = ''
    for i in range(len(digest)):
        h_string += digest[i]
        if i%2 == 1:
            h_string += ' '
    res += h_string[:47]+'\n'
    res += h_string[48:]+'\n\n\n'
    res += "Je confirme par la présente la clé publique ci-dessus pour ma signature électronique.\n\n"
    res += "Date :                  Nom/Entreprise :                Signature :"
    return res

def compute_X509cert_hash(cert):
    c = binascii.hexlify(cert.decode('base64'))
    if len(c)%2 == 1:
        c = '0'+c
    t = []
    tmp = ''
    for i in c :
        tmp += i
        if len(tmp) == 2:
            t.append(int(tmp, 16))
            tmp = ''
    h= bytes(bytearray(t))
    digest = binascii.hexlify(SHA256.new(h).digest()).upper()
    return digest


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
