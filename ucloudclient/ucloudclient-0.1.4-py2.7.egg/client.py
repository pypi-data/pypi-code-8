'''
ucloud python sdk client.
'''
from api import umon, unet, uhost
from utils import base


class Client(object):
    '''
    ucloud python sdk client.
    '''
    def __init__(self,base_url,public_key,private_key,debug=False,timing=False):
        self.base_url=base_url
        self.private_key=private_key
        self.public_key=public_key

        self.uhost= uhost.UhostManager(self)
        self.unet= unet.UnetManager(self)
        self.umon= umon.UnetManager(self)

        self.client= base.HTTPClient(base_url,debug,timing)


    def get_timings(self):
        return self.client.get_timing()

