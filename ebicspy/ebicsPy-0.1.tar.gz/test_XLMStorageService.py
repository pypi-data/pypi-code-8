# -*- coding: utf-8 -*-
from ebicspy import *

storage = XMLStorageService('./keys/yuntux2.xml')
logger = FileSystemLogger()
bank = Bank(storage, 'testBank88', 'https://server-ebics.webank.fr', 28103, '/WbkPortalFileTransfert/EbicsProtocol', 'EBIXQUAL')
partner = Partner(storage, 'testPartner82', 'YUNDU', 'YUNDU', logger)

def send_partner_keys(partner, bank):
    partner.createPartnerKeys()
    print "========== PARTNER KEY GENERATION OK =========="
    partner.handle_ini_exchange(bank)
    print "========== INI MESSAGE SENT =========="
    print "========== WE HAVE NOW TO SEND THE HIA MESSAGE =========="
    partner.handle_hia_exchange(bank)
    print "========== HIA MESSAGE SENT =========="
    print "===>>> YOU HAVE TO SEND INITIATION LETTERS TO YOUR BANK BEFORE DOWNLOADING THE BANK KEYS"
    partner.storageService.setStatus("bank_init")

def get_bank_keys(partner, bank):
    partner.loadPartnerKeys()
    bank_auth_key_hash = partner.storageService.getBankAuthKeyHash()
    bank_encrypt_key_hash = partner.storageService.getBankEncryptKeyHash()
    hpb_exchange(partner, bank, bank_auth_key_hash, bank_encrypt_key_hash)
    partner.storageService.setStatus("ready")

def send_file(partner, bank):
    partner.loadPartnerKeys()
    partner.loadBankKeys(bank)
#    fileUpload_from_fileSystem(partner, bank, "/home/yuntux/helloWorld.txt","pain.xxx.cfonb160.dct", "fileName", True)
    fileUpload_from_fileSystem(partner, bank, "/home/yuntux/fileup","pain.xxx.cfonb160.dct", "fileName", True)
#    fileUpload_from_fileSystem(partner, bank, "/home/yuntux/order_old","pain.xxx.cfonb160.dct", "fileName", True)

def get_file(partner, bank):
    partner.loadPartnerKeys()
    partner.loadBankKeys(bank)
    fileDownload_to_fileSystem(partner, bank, "/home/yuntux/")

#send_partner_keys(partner, bank)
#get_bank_keys(partner, bank)
#send_file(partner, bank)
#get_file(partner, bank)

