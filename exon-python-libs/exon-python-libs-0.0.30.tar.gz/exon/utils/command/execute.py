__author__ = 'Stephan Conrad <stephan@conrad.pics>'

import envoy;

class CommandOut(object):
    def __init__(self):
        self.stdout = None
        self.stderr = None
        self.rc = -1

def exec(command=""):
    cmd = envoy.run(command)
    ret = CommandOut()
    ret.rc = cmd.status_code
    ret.stdout = cmd.std_out.split("\n")
    ret.stderr = cmd.std_err.split("\n")
    return ret
