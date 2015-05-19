#!/usr/bin/env python2
"""
Handles emailing - for alerts, reports, etc

Todo:
    - add throttling
    - add script to run from shell scripts
    - add script alerter
"""
import os, sys
import smtplib
import time
import errno
import logging
from datetime import datetime


class Sender(object):

    def __init__(self,
                 smtp_address,
                 user,
                 passwd,
                 log_name='__main__'):
        """
        args:
            - smtp_address: ex: 'smtp.gmail.com:587'
            - user:         ex: foo@gmail.com
            - passwd:       ex: blahblah
        """

        self.smtp_address = smtp_address
        self.user         = user
        self.passwd       = passwd

        self.logger = logging.getLogger('%s.cletus_sender' % log_name)
        self.logger.debug('Sender starting now')


    def send(self, from_addr, to_addr, subject, msg):
        """ 
        """
        server = smtplib.SMTP(self.smtp_address)
        server.starttls()
        server.login(self.user, self.passwd)

        send_date = datetime.strftime(datetime.now(), '%Y-%m-%d')
        header = "Date: %s\r\nFrom: %s\r\nTo: %s\r\nSubject: %s\r\nX-Mailer: My-Mail\r\n\r\n" \
             % (send_date, from_addr, to_addr, subject)
        server.sendmail(from_addr, to_addr, header+msg)
        server.quit()
        self.logger.info('msg sent')

