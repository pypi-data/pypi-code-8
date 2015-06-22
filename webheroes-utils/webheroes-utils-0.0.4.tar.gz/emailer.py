
#
# WebHeroes-Utils -- Web Heroes Inc. python utility module
#
# Copyright (c) 2015, Web Heroes Inc..
#
# WebHeroes-Utils is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.  See the LICENSE file at the top of the source tree.
#
# WebHeroes-Utils is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#

__author__                      = "Matthew Brisebois"
__email__                       = "matthew@webheroes.ca"
__copyright__                   = "Copyright (c) 2015 Web Heroes Inc."
__license__                     = "Dual License: GPLv3 (or later) and Commercial (see LICENSE)"

__all__				= ["send"]

import smtplib
from .			import logging
from email.mime.text	import MIMEText

log			= logging.getLogger('emailer')
log.setLevel(logging.ERROR)

def send( to=None, message=None ):
    sender		= ''
    msg			= MIMEText(message, "html")
    msg['Subject']	= ''
    msg['From']		= sender
    msg['To']		= to
    log.debug( "sending email to: %s with mailgun: %s", to, msg )

    # s			= smtplib.SMTP( "localhost" )
    # v			= s.sendmail(sender, [to], message)

    s			= smtplib.SMTP('smtp.mailgun.org', 587)
    s.login('<email>', '<password>')
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()
    return True
