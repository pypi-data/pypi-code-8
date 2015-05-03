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

from Crypto.PublicKey import RSA
import hashlib
from crypto_tools import *
from ini_step import *
from hia_step import *
from hpb_step import *

class Bank :
    def __init__(self, storageService, name, urlHost, urlPort, urlRoot, hostId) :
        self.name = name
        self.urlHost = urlHost
        self.urlPort = urlPort
        self.urlRoot = urlRoot
        self.hostId = hostId
        self.storageService = storageService


    def getHostId (self) :
        return self.hostId

    def getUrlHost (self) :
        return self.urlHost

    def getUrlPort (self) :
        return self.urlPort

    def getUrlRoot (self) :
        return self.urlRoot

    def import_TLSCertificate(self, path):
        #FIXME : check the TLS certificate each time we send/receive data from/to the bank
        print "TODO"

    def setAuthKey (self, authKey) :
        self.authKey = authKey

    def getKeyHash(self, bankKey):
        #The SHA-256 hash values of the financial institution's public keys for X002 and
        #E002 are composed by concatenating the exponent with a blank character and the
        #modulus in hexadecimal representation (using lower case letters) without leading
        #zero (as to the hexadecimal representation). The resulting string has to be
        #converted into a byte array based on US ASCII code

        n_long = getattr(bankKey.key, 'n')
        n_hex_str = str(hex(n_long))[2:-1]

        e_long = getattr(bankKey.key, 'e')
        e_hex_str = str(hex(e_long))[2:-1]

        s = e_hex_str + ' ' + n_hex_str
        if s[0] == '0':
            s = s[1:]

        m = hashlib.sha256()
        m.update(s)
        string_digest = m.digest()

        res = string_digest.encode('base64')
        return res.strip()
        
    def saveKeys(self, auth_certificate, auth_modulus, auth_exponent, auth_version, encrypt_certificate, encrypt_modulus, encrypt_exponent, encrypt_version):
        self.storageService.saveBankKey("auth", auth_version, auth_modulus, auth_exponent, auth_certificate)
        self.storageService.saveBankKey("encrypt", encrypt_version, encrypt_modulus, encrypt_exponent, encrypt_certificate)

    def getAuthKey (self) :
        return self.authKey

    def setSignKey (self, signKey) :
        self.signKey = signKey

    def getSignKey (self) :
        return self.signKey

    def setEncryptKey (self, encryptKey) :
        self.encryptKey = encryptKey

    def getEncryptKey (self) :
        return self.encryptKey

    def getName (self) :
        return self.name

class Partner : 
    def __init__(self, storageService, name, partnerId, userId, fileExchangedLogger, ebicsProfile="T"):
        self.name = name
        self.partnerId = partnerId
        self.userId = userId
        self.ebicsProfile = ebicsProfile
        self.fileExchangedLogger = fileExchangedLogger
        self.storageService = storageService

    def handle_ini_exchange(self, bank):
        ini_exchange(self, bank)
        #TODO check the validity of the response
        ini_sign_letter = letter("INI",
            "Certificat pour la signature électronique (A005)" , 
            self.getSignCertificate(),
            bank.getHostId(), 
            self.getUserId(), 
            self.getPartnerId())
        self.storageService.saveLetter(ini_sign_letter, "ini_letter_sign")

    def handle_hia_exchange(self, bank):
        hia_exchange(self, bank)
        #TODO check the validity of the response
        hia_encrypt_letter = letter("HIA",
            "Certificat pour le chiffrement (E002)" , 
            self.getEncryptCertificate(),
            bank.getHostId(), 
            self.getUserId(), 
            self.getPartnerId())
        self.storageService.saveLetter(hia_encrypt_letter, "hia_letter_encrypt")
        hia_auth_letter = letter("HIA",
            "Certificat pour l'authentification (X002)" , 
            self.getAuthCertificate(),
            bank.getHostId(), 
            self.getUserId(), 
            self.getPartnerId())
        self.storageService.saveLetter(hia_auth_letter, "hia_letter_auth")
        #TODO display the ini letter file path
    

    def init(self, bank):
        status = self.storageService.getStatus()

        if satus == "partner_init":
            self.createPartnerKeys()
            print "========== PARTNER KEY GENERATION OK =========="        
            self.handle_ini_exchange(bank)
            print "========== INI MESSAGE SENT =========="
            print "========== WE HAVE NOW TO SEND THE HIA MESSAGE =========="
            self.handle_hia_exchange(bank)
            print "========== HIA MESSAGE SENT =========="
            print "===>>> YOU HAVE TO SEND INITIATION LETTERS TO YOUR BANK BEFORE DOWNLOADING THE BANK KEYS"
            
        else :
            self.loadPartnerKeys()
            print "========== PARTNER KEYS AND CERTIFICATES LOADED =========="

            if satus == "bank_init":
                bank_auth_key_hash = self.storageService.getBankAuthKeyHash()
                bank_encrypt_key_hash = self.storageService.getBankEncryptKeyHash()
                hpb_exchange(self, bank, bank_auth_key_hash, bank_encrypt_key_hash)

            else :
                self.loadBankKeys(bank)
                print "========== BANK KEYS AND CERTIFICATES LOADED =========="

    def getEbicsProfile (self) :
        return self.ebicsProfile

    def getFileExchangedLogger (self) :
        return self.fileExchangedLogger
        
    def getName (self) :
        return self.name

    def getPartnerId (self) :
        return self.partnerId

    def getUserId (self) :
        return self.userId

    def setAuthKey (self, private, public) :
        self.authPrivateKey= private
        self.authPublicKey = public

    def getAuthPrivateKey (self) :
        return self.authPrivateKey

    def getAuthPublicKey (self) :
        return self.authPublicKey

    def setSignKey (self, private, public) :
        self.signPrivateKey = private
        self.signPublicKey = public

    def getSignPrivateKey (self) :
        return self.signPrivateKey

    def getSignPublicKey (self) :
        return self.signPublicKey

    def setEncryptKey (self, private, public) :
        self.encryptPrivateKey = private
        self.encryptPublicKey = public

    def getEncryptPrivateKey (self) :
        return self.encryptPrivateKey

    def getEncryptPublicKey (self) :
        return self.encryptPublicKey

    #FIXME : the two followinig aliases are used for cryptographique roudTest purpose only
    def getAuthKey (self) :
        return self.authPublicKey
    def getEncryptKey (self) :
        return self.encryptPublicKey
    def getKeyHash(self, bankKey):
        return "FEA76AAE939D0CC0B82657C10D3E253E"
    def getHostId(self):
        return "EBIXQAL"

    def setSignCertificate (self, certificate):
        self.signCertificate = certificate

    def getSignCertificate (self):
        return self.signCertificate

    def setAuthCertificate (self, certificate):
        self.authCertificate = certificate

    def getAuthCertificate (self):
        return self.authCertificate

    def setEncryptCertificate (self, certificate):
        self.encryptCertificate = certificate

    def getEncryptCertificate (self):
        return self.encryptCertificate

    def createPartnerKeys(self):
        auth_private, auth_public, auth_cert = create_rsa_key(AUTH_KEY_LENGTH, "auth", self.storageService)
        if self.ebicsProfile == "T" :
            sign_private, sign_public, sign_cert = create_rsa_key(SIGN_KEY_LENGTH, "sign", self.storageService) 
        encrypt_private, encrypt_public, encrypt_cert = create_rsa_key(ENCRYPT_KEY_LENGTH, "encrypt", self.storageService) 
        self.loadPartnerKeys()

    def loadPartnerKeys(self):
        auth_modulus = self.storageService.getPartnerKeyComponent("modulus", "auth")
        auth_public_exponent = self.storageService.getPartnerKeyComponent("public_exponent", "auth")
        auth_private_exponent = self.storageService.getPartnerKeyComponent("private_exponent", "auth")
        self.setAuthKey(RSA.construct((auth_modulus, auth_public_exponent, auth_private_exponent)), RSA.construct((auth_modulus, auth_public_exponent)))

        sign_modulus = self.storageService.getPartnerKeyComponent("modulus", "sign")
        sign_public_exponent = self.storageService.getPartnerKeyComponent("public_exponent", "sign")
        sign_private_exponent = self.storageService.getPartnerKeyComponent("private_exponent", "sign")
        self.setSignKey(RSA.construct((sign_modulus, sign_public_exponent, sign_private_exponent)), RSA.construct((sign_modulus, sign_public_exponent)))
            
        encrypt_modulus = self.storageService.getPartnerKeyComponent("modulus", "encrypt")
        encrypt_public_exponent = self.storageService.getPartnerKeyComponent("public_exponent", "encrypt")
        encrypt_private_exponent = self.storageService.getPartnerKeyComponent("private_exponent", "encrypt")
        self.setEncryptKey(RSA.construct((encrypt_modulus, encrypt_public_exponent, encrypt_private_exponent)), RSA.construct((encrypt_modulus, encrypt_public_exponent)))

        sign_cert = self.storageService.getPartnerCertificate('sign')
        self.setSignCertificate(sign_cert)
        auth_cert = self.storageService.getPartnerCertificate('auth')
        self.setAuthCertificate(auth_cert)
        encrypt_cert = self.storageService.getPartnerCertificate('encrypt')
        self.setEncryptCertificate(encrypt_cert)


    def loadBankKeys(self, bank):
        auth_modulus = self.storageService.getBankKeyComponent("modulus", "auth")
        auth_exponent = self.storageService.getBankKeyComponent("public_exponent", "auth")
        bank.setAuthKey(RSA.construct((auth_modulus, auth_exponent)))
        encrypt_modulus = self.storageService.getBankKeyComponent("modulus", "encrypt")
        encrypt_exponent = self.storageService.getBankKeyComponent("public_exponent", "encrypt")                
        bank.setEncryptKey(RSA.construct((encrypt_modulus, encrypt_exponent)))


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
