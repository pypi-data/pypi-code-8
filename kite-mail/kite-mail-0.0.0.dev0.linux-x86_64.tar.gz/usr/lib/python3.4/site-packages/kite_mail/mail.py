#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import pyzmail

class kiteMail(object):

    def __init__(self, raw_mail):
        self.raw_mail = raw_mail

        self.factory  = self._migrate_mailfactory()
        self.content_encode = self._get_content_encode()

    def _migrate_mailfactory(self):
        return pyzmail.PyzMessage.factory(self.raw_mail)

    def _get_content_encode(self):
        header_content_type = self.factory.get_decoded_header('content-type')
        _result = re.search(r'charset=(\S+)', header_content_type)
        return _result.group(1).lower()

    def get_mailpart(self):

        msg = self.factory

        if msg.text_part:
            _result = msg.text_part.get_payload()
        elif msg.text_html:
            _result = msg.html_part.get_payload()

        if not self.content_encode== None:
            return _result.decode(self.content_encode)

        return _result


