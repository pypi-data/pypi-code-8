import subprocess
import os
import saddle
import sys

# TODO: Create email object to signify received mail.
# TODO: "Wait until email arrives" function.

class SaddleSMTPService(saddle.Service):
    def __init__(self, service_engine, python=sys.executable, port=10025, needs=None):
        super(SaddleSMTPService, self).__init__(
            service_engine,
            name="SaddleSMTP",
            command=[python, "-u", "-m", "saddlesmtp.smtp", "--port", str(port)],
            readysignal={
                'logline': lambda line: "SMTP Server running" in line,
            },
            needs=needs,
        )

    def setup(self):
        pass

    def poststart(self):
        pass
