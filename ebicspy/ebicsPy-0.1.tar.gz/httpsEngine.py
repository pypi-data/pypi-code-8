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

import httplib
import urllib2
import os
from tools import *
os.environ['http_proxy'] = ''

class HTTPSEngine :
    def __init__(self, partner, bank) :
        self.bank = bank
        self.partner = partner
        self.fileExchangedLogger = partner.getFileExchangedLogger()

    def send(self, xml):
        #TODO : check xml with xsd ? redondant ?
        url_host = self.bank.getUrlHost()
        url_port = self.bank.getUrlPort()
        url_root = self.bank.getUrlRoot()
        whole_url = url_host+':'+str(url_port)+url_root

        #TODO : check server certificate validity with the CA chain
        xml_utf8 = xml #TODO : check utf8 
        
        self.fileExchangedLogger.logMessage('archive', 'request_'+get_timestamp()+'.xml', xml_utf8)

        # TODO : verify the server certificate before exchange files
        headers = {"Content-type": "text/xml; charset=UTF-8", "Accept": "text/xml", "Content-length" : str(len(xml_utf8))}
        request = urllib2.Request(whole_url, headers=headers)
        request.get_method = lambda: 'POST'
        request.add_data(xml_utf8)
        response = urllib2.urlopen(request)
        response_content = response.read()
        print response.info()
        
        self.fileExchangedLogger.logMessage('archive', 'response_'+get_timestamp()+'.xml', response_content)
        
        return response_content

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
