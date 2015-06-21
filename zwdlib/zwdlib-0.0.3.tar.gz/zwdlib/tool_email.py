# -*- coding: utf8 -*-

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tool_env import get_filename_by_path
import os
import smtplib
import time



# EMAIL_HOST="smtp.exmail.qq.com"
# EMAIL_PORT= 25
# EMAIL_HOST_USER="support@jinbangqm.com"
# EMAIL_HOST_PASSWORD="jinbangqm520"

EMAIL_HOST="smtp.qq.com"
EMAIL_PORT= 25
EMAIL_HOST_USER="liqiang239@qq.com"
EMAIL_HOST_PASSWORD="liqiangbobcj"


class SendMail():

    def __init__(self,
                 subject,
                 content,
                 to_list,
                 attach_list=[],
                 tls=True,
                 encoding='utf-8',
                 retry=3,
                 email_host=EMAIL_HOST,
                 email_port=EMAIL_PORT,
                 email_host_user=EMAIL_HOST_USER,
                 email_host_password=EMAIL_HOST_PASSWORD,
                 ):
        self.subject = subject
        self.content = content
        self.to_list = to_list
        self.attach_list = attach_list
        self.tls = tls
        self.encoding = encoding
        self.retry = retry
        self.email_host = email_host
        self.email_port = email_port
        self.email_host_user = email_host_user
        self.email_host_password = email_host_password
        self.msg = None
        
    # load base info of email 
    def load_base_msg(self):
        self.msg = MIMEMultipart()
        self.msg['from'] = self.email_host_user
        self.msg['to'] = ','.join(self.to_list)
        self.msg['subject'] = self.subject
#         self.msg.attach(MIMEText(self.content, 'plain', 'utf-8'))
        self.msg.attach(MIMEText(self.content, 'html', 'utf-8'))


    # load attach of email
    def load_attach(self):
        for path in self.attach_list:
#             print path
            if not os.path.lexists(path):
                fp = open(path,'w')
                fp.close()
            att = MIMEText(open(path, 'rb').read(), 'base64', self.encoding)
            att["Content-Type"] = 'application/octet-stream'
            att["Content-Disposition"] = 'attachment; filename="%s"' % get_filename_by_path(path)
            self.msg.attach(att)

    def load_msg(self):
        self.load_base_msg()
        self.load_attach()
    
    def send(self):
        
        self.load_msg()
        smtp = smtplib.SMTP() 
        
        while 1:
            try:
                print self.email_host
                print self.email_port
                smtp.connect(self.email_host, self.email_port)
                break
            except:
                print 'conntent smtp failed'
                time.sleep(60)
        if self.tls:
            smtp.starttls() # Put the SMTP connection in TLS (Transport Layer Security) mode. All SMTP commands that follow will be encrypted.
        smtp.login(self.email_host_user, self.email_host_password)
        while 1:
            if self.retry:
                try:
                    print self.msg.as_string()
                    smtp.sendmail(self.email_host_user, self.to_list, self.msg.as_string()) 
                    print 'send sucess'
                    break
                except Exception,e:
                    self.retry -= 1
                    print e
                    time.sleep(3)
            else:
                break
        smtp.quit()
 
    
if __name__ == "__main__":
    subject = 'final test email'
    content = '<h1>hello world</h1>'
    to_list = ['liqiang239@qq.com']
    attach_list = ['E:/a/a.txt']
#     sm = SendMail(subject,content,to_list,attach_list=attach_list)
    sm = SendMail(subject,content,to_list)
    sm.send()
