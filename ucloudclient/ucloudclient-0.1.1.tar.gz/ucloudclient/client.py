'''
ucloud python sdk client.
'''
from api import umon, unet, uhost
from utils import base


class Client(object):
    '''
    ucloud python sdk client.
    '''
    def __init__(self,base_url,public_key,private_key,timming=False):
        self.base_url=base_url
        self.private_key=private_key
        self.public_key=public_key

        self.uhost= uhost.UhostManager(self)
        self.unet= unet.UnetManager(self)
        self.umon= umon.UnetManager(self)

        self.client= base.HTTPClient(base_url,timming)


    def get_timings(self):
        return self.client.get_timing()


if __name__=='__main__':
    public_key='asdf'
    private_key='asdf'
    base_url='https://api.ucloud.cn'

    region='cn-north-03'
    # region='us-west-01'
    c=Client(base_url,public_key,private_key)
    image_id='uimage-3gzxij'
    #print(c.uhost.get_price(region,image_id,2,2048,1,'Month'))
    # Parameters={
    #         "time_range":"2592000",
    #         "metric_names":["BandOut"],
    #         "resource_type":"sharebandwidth",
    #         "resourceid":"",
    #         }
    # #print(c.umon.metric_get(region,**Parameters))
    images= c.uhost.get_image(region)
    print images
        #print('OsName:%s, ImageId:%s'%(i['OsName'],i['ImageId']))

    # Parameters={
    #         "region":"cn-north-03",
    #         "imageid":"uimage-3gzxij",
    #         "loginmode":"Password",
    #         "password":"MTIzNDU2NzgK",
    #         }
    # print(c.uhost.create(**Parameters))

    # print(c.uhost.get(region))
